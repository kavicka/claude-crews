"""Run one benchmark attempt of the coupon task and score it.

    python3 bench/run.py <variant> <n> [--workroot DIR]

Variants:
  vibe-medium  the task sentence alone, Opus at medium effort (the default)
  vibe-xhigh   the task sentence alone, Opus at xhigh effort
  crew         the task sentence through /crew:ship (plugins/crew from this repo)

Each attempt starts from a fresh copy of ../base with its own git repo, runs
`claude -p` headless with a sanitised environment and a narrow tool allowlist,
then saves the real patch, the transcript and the score to results/<variant>-<n>/.
The hidden tests are copied in only after the agent has finished.
"""
import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEMO = HERE.parent
REPO = DEMO.parent.parent
sys.path.insert(0, str(HERE))
from score import score  # noqa: E402

TASK = ("Let checkout accept several coupon codes at once: "
        "`checkout(items, codes?: string | string[], now?)`. A single string must keep working.")

# The crew's only stop is the plan checkpoint. Nobody watches a benchmark run, so the
# operator answers it the same way for every attempt: take the planner's defaults.
OPERATOR = ("Benchmark run: no human is watching. At the checkpoint, do not stop and wait. "
            "Accept the planner's default for every open question and fold in the skeptic's "
            "changes, list those decisions in your final summary, and continue to the end. "
            "Do not commit.")

VARIANTS = {
    "vibe-medium": {"prompt": TASK, "effort": "medium", "plugin": False},
    "vibe-xhigh": {"prompt": TASK, "effort": "xhigh", "plugin": False},
    "crew": {"prompt": f"/crew:ship {TASK}\n\n{OPERATOR}", "effort": None, "plugin": True},
}

# Enough to edit files, run the project's tests and typecheck, and read git state.
ALLOWED = ["Bash(npm test*)", "Bash(npm run *)", "Bash(npx vitest*)", "Bash(npx tsc*)",
           "Bash(git diff*)", "Bash(git status*)", "Bash(git log*)", "Bash(git show*)",
           "Bash(ls*)", "Bash(node -e*)"]
# Tools of the cloud session this benchmark ran in that a normal user doesn't have, and
# anything that could see the hidden tests in this repository.
DENIED = ["Workflow", "Skill", "Artifact", "ArtifactComments", "ArtifactData", "SendUserFile",
          "PushNotification", "CronCreate", "ScheduleWakeup", "DesignSync", "WebFetch", "WebSearch",
          f"Read(/{REPO}/**)"]
KEEP_ENV = ["PATH", "HOME", "LANG", "TERM", "ANTHROPIC_BASE_URL", "HTTPS_PROXY", "https_proxy",
            "NO_PROXY", "no_proxy", "NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE", "CURL_CA_BUNDLE",
            "REQUESTS_CA_BUNDLE"]


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True, **kw)


def prepare(work: Path, node_modules: Path) -> None:
    shutil.copytree(DEMO / "base", work, ignore=shutil.ignore_patterns("node_modules"))
    shutil.copytree(node_modules, work / "node_modules", symlinks=True)
    (work / ".gitignore").write_text("node_modules/\n")
    git = ["git", "-c", "user.name=bench", "-c", "user.email=bench@example.invalid"]
    sh(["git", "init", "-q"], work)
    sh(["git", "add", "-A"], work)
    sh(git + ["commit", "-qm", "base"], work)


def subagent_calls(lines: list[str]) -> list[str]:
    """subagent_type of every Task/Agent call the main session made, in order."""
    calls = []
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant" or event.get("parent_tool_use_id"):
            continue
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "tool_use" and block.get("name") in ("Task", "Agent"):
                calls.append(block.get("input", {}).get("subagent_type", "general-purpose"))
    return calls


def node_modules_cache(root: Path) -> Path:
    cache = root / "_node_modules" / "base"
    if not (cache / "node_modules").exists():
        shutil.copytree(DEMO / "base", cache, ignore=shutil.ignore_patterns("node_modules"),
                        dirs_exist_ok=True)
        sh(["npm", "ci", "--silent", "--no-audit", "--no-fund"], cache)
    return cache / "node_modules"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("variant", choices=VARIANTS)
    ap.add_argument("n", type=int)
    ap.add_argument("--workroot", type=Path, default=Path(tempfile.gettempdir()) / "coupon-bench")
    ap.add_argument("--timeout", type=int, default=45 * 60)
    args = ap.parse_args()

    v = VARIANTS[args.variant]
    name = f"{args.variant}-{args.n}"
    out = HERE / "results" / name
    if out.exists():
        print(f"{out} exists, skipping")
        return 0
    work = args.workroot / name
    shutil.rmtree(work, ignore_errors=True)
    args.workroot.mkdir(parents=True, exist_ok=True)
    prepare(work, node_modules_cache(args.workroot))

    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    if v["effort"]:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = v["effort"]
    cmd = ["claude", "-p", v["prompt"], "--model", "opus", "--output-format", "stream-json",
           "--verbose", "--strict-mcp-config", "--permission-mode", "acceptEdits",
           "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED]
    if v["plugin"]:
        cmd += ["--plugin-dir", str(REPO / "plugins" / "crew")]

    started = time.time()
    proc = subprocess.run(cmd, cwd=work, env=env, text=True, capture_output=True, timeout=args.timeout)
    wall = time.time() - started

    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    result = {}
    for line in reversed(lines):
        if '"type":"result"' in line:
            try:
                result = json.loads(line)
                break
            except json.JSONDecodeError:
                pass
    transcript = "\n".join(lines)
    leaked = any(s in transcript for s in ("acceptance.test", "/coupon-demo/hidden", "crew-run/", "vibe.diff"))
    subagents = subagent_calls(lines)

    sh(["git", "add", "-A"], work)
    patch = sh(["git", "diff", "--cached", "HEAD"], work).stdout

    out.mkdir(parents=True)
    (out / "changes.patch").write_text(patch)
    with gzip.open(out / "transcript.jsonl.gz", "wt") as fh:
        fh.write(transcript + "\n")
    if proc.stderr.strip():
        (out / "stderr.txt").write_text(proc.stderr[-20000:])
    (out / "final-answer.md").write_text(result.get("result", "") + "\n")

    usage = result.get("modelUsage", {})
    record = {
        "variant": args.variant,
        "n": args.n,
        "exit_code": proc.returncode,
        "wall_seconds": round(wall, 1),
        "cost_usd": result.get("total_cost_usd"),
        "num_turns": result.get("num_turns"),
        "tokens_by_model": {m: {k: u.get(k, 0) for k in ("inputTokens", "outputTokens", "cacheReadInputTokens",
                                                       "cacheCreationInputTokens")}
                            for m, u in usage.items()},
        "subagents": subagents,
        "hidden_test_leak_suspected": leaked,
        "score": score(work),
    }
    (out / "result.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("variant", "n", "exit_code", "wall_seconds", "cost_usd")}
                     | {"hidden": record["score"]["hidden_passed"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

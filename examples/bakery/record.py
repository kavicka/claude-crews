"""Record the bakery story: three real claude-crews runs in one isolated home.

    python3 record.py setup                       # fresh home with the fictional knowledge base and site
    python3 record.py run council                  # step 1: /council:vote
    python3 record.py run quote                    # step 2: /office:quote
    python3 record.py run crew                     # step 3: /crew:ship
    python3 record.py answer <step> <file.md>      # resume a step that stopped with questions

The home lives outside this repository (default: $TMPDIR/bakery-story/home). Claude Code
runs headless with that HOME, so `~/knowledge` is Lucia's fictional knowledge base and
nothing from the real user's setup is visible. Each phase's transcript, final answer and
cost go to runs/<step>/<phase>-*. Answers to the agents' questions are written by the
person recording the example, playing Lucia; they are saved next to the questions.
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
REPO = HERE.parent.parent
ROOT = Path(os.environ.get("BAKERY_ROOT", Path(tempfile.gettempdir()) / "bakery-story"))
HOME = ROOT / "home"
SITE = HOME / "code" / "kvasok-site"
RUNS = HERE / "runs"

STEPS = {
    "council": {
        "prompt": "/council:vote Should the bakery launch with online payments or start with pay-at-pickup?",
        "cwd": HOME,
        "plugins": ["council", "office"],
    },
    "quote": {
        "prompt": "/office:quote one-page online ordering site for a bakery, Slovak + English, contact form to email",
        "cwd": HOME,
        "plugins": ["office", "council"],
    },
    "crew": {
        "prompt": "/crew:ship add online ordering with pickup time slots to the bakery website",
        "cwd": SITE,
        "plugins": ["crew"],
    },
}

ALLOWED = ["Bash(npm test*)", "Bash(npm run *)", "Bash(npm install*)", "Bash(npx vitest*)", "Bash(npx tsc*)",
           "Bash(git diff*)", "Bash(git status*)", "Bash(git log*)", "Bash(git show*)", "Bash(git rev-parse*)",
           "Bash(git ls-files*)", "Bash(ls*)", "Bash(date*)", "Bash(node -e*)", "WebSearch", "WebFetch"]
DENIED = ["Workflow", "CronCreate", "CronDelete", "RemoteTrigger", "ScheduleWakeup", "PushNotification",
          "DesignSync", f"Read(/{REPO}/**)"]
KEEP_ENV = ["PATH", "LANG", "TERM", "ANTHROPIC_BASE_URL", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy",
            "NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE", "CURL_CA_BUNDLE", "REQUESTS_CA_BUNDLE"]


def git(*args: str, cwd: Path) -> str:
    base = ["git", "-c", "user.name=Lucia", "-c", "user.email=lucia@lucia-dev.example"]
    return subprocess.run(base + list(args), cwd=cwd, check=True, capture_output=True, text=True).stdout


def setup() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    shutil.copytree(HERE / "knowledge", HOME / "knowledge")
    shutil.copytree(HERE / "site", SITE, ignore=shutil.ignore_patterns("node_modules"))
    subprocess.run(["npm", "ci", "--silent", "--no-audit", "--no-fund"], cwd=SITE, check=True)
    (SITE / ".gitignore").write_text("node_modules/\n")
    git("init", "-q", cwd=SITE)
    git("add", "-A", cwd=SITE)
    git("commit", "-qm", "One-page site with contact form", cwd=SITE)
    print(f"home ready: {HOME}")


def state_file(step: str) -> Path:
    return RUNS / step / "state.json"


def run_claude(step: str, prompt: str, resume: str | None) -> None:
    cfg = STEPS[step]
    out = RUNS / step
    out.mkdir(parents=True, exist_ok=True)
    state = json.loads(state_file(step).read_text()) if state_file(step).exists() else {"phases": []}
    phase = len(state["phases"]) + 1

    cmd = ["claude", "-p", prompt, "--model", "opus", "--output-format", "stream-json", "--verbose",
           "--strict-mcp-config", "--permission-mode", "acceptEdits",
           "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED]
    for plugin in cfg["plugins"]:
        cmd += ["--plugin-dir", str(REPO / "plugins" / plugin)]
    if resume:
        cmd += ["--resume", resume]
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ} | {"HOME": str(HOME)}

    started = time.time()
    proc = subprocess.run(cmd, cwd=cfg["cwd"], env=env, text=True, capture_output=True, timeout=90 * 60)
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    result = {}
    for line in reversed(lines):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            result = event
            break

    with gzip.open(out / f"{phase}-transcript.jsonl.gz", "wt") as fh:
        fh.write("\n".join(lines) + "\n")
    (out / f"{phase}-prompt.md").write_text(prompt + "\n")
    (out / f"{phase}-answer.md").write_text(result.get("result", "") + "\n")
    if proc.stderr.strip():
        (out / f"{phase}-stderr.txt").write_text(proc.stderr[-20000:])
    state["phases"].append({
        "phase": phase,
        "session_id": result.get("session_id"),
        "exit_code": proc.returncode,
        "wall_seconds": round(time.time() - started, 1),
        "cost_usd": result.get("total_cost_usd"),
        "num_turns": result.get("num_turns"),
    })
    state_file(step).write_text(json.dumps(state, indent=2) + "\n")
    print(json.dumps(state["phases"][-1]))
    print(result.get("result", "")[-6000:])


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    r = sub.add_parser("run")
    r.add_argument("step", choices=STEPS)
    a = sub.add_parser("answer")
    a.add_argument("step", choices=STEPS)
    a.add_argument("file", type=Path)
    args = ap.parse_args()

    if args.cmd == "setup":
        setup()
    elif args.cmd == "run":
        run_claude(args.step, STEPS[args.step]["prompt"], None)
    else:
        state = json.loads(state_file(args.step).read_text())
        run_claude(args.step, args.file.read_text().strip(), state["phases"][-1]["session_id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

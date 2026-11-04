"""Turn the recorded transcripts into readable conversation logs.

    python3 extract.py            # writes runs/<step>/conversation.md for every recorded step

Shows, in order: what you typed, what the main session said, every brief it sent to an
agent, what each agent returned, and the questions it put to you with your answers.
Tool calls inside the agents are summarised by count, not printed.
"""
import gzip
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
HOME_PATH = re.compile(r"/tmp/[^\s`'\"]*?/home/")


def clean(text: str) -> str:
    text = HOME_PATH.sub("~/", text)
    # Drop the harness frame around subagent hand-backs and internal async notices.
    text = re.sub(r"<tools-used-before-summary>.*?</tools-used-before-summary>\s*", "", text, flags=re.S)
    text = re.sub(r"\[Subagent hand-back\].*?The report follows:\s*", "", text, flags=re.S)
    text = re.sub(r"\n  ", "\n", text)
    return text.strip()


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in clean(text).splitlines())


def phase_log(path: Path, prompt: str, phase: int) -> list[str]:
    out = [f"## Phase {phase}", "", "**You:**", "", quote(prompt), ""]
    names: dict[str, str] = {}
    tasks: dict[str, str] = {}
    shown: set[str] = set()
    inner_tools: Counter = Counter()
    for line in gzip.open(path, "rt"):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        parent = e.get("parent_tool_use_id")
        if e.get("type") == "assistant" and parent:
            for b in e["message"]["content"]:
                if b.get("type") == "tool_use":
                    inner_tools[(names.get(parent, "agent"), b["name"])] += 1
            continue
        if e.get("type") == "assistant":
            for b in e["message"]["content"]:
                if b.get("type") == "text" and b["text"].strip():
                    out += ["**Main session:**", "", quote(b["text"]), ""]
                if b.get("type") == "tool_use" and b["name"] == "SendMessage":
                    agent = tasks.get(b["input"].get("to", ""), "an agent")
                    names[b["id"]] = agent
                    msg = b["input"].get("message", "")
                    out += [f"<details><summary>→ follow-up to <b>{agent}</b>: {b['input'].get('summary', '')}</summary>",
                            "", quote(msg if isinstance(msg, str) else json.dumps(msg)), "", "</details>", ""]
                if b.get("type") == "tool_use" and b["name"] in ("Agent", "Task"):
                    agent = b["input"].get("subagent_type", "general-purpose")
                    names[b["id"]] = agent
                    out += [f"<details><summary>→ brief to <b>{agent}</b>: {b['input'].get('description', '')}</summary>",
                            "", quote(b["input"].get("prompt", "")), "", "</details>", ""]
        elif e.get("type") == "user" and not parent and isinstance(e["message"]["content"], list):
            for b in e["message"]["content"]:
                if b.get("type") == "tool_result" and b.get("tool_use_id") in names:
                    body = text_of(b["content"])
                    if "Async agent launched" in body:
                        out += [f"*{names[b['tool_use_id']]} is working in the background.*", ""]
                    elif '"resumedAgentId"' in body or body.strip().startswith('{"success"'):
                        continue  # SendMessage acknowledgement; the reply arrives as a notification
                    elif clean(body)[:200] in shown:
                        continue
                    else:
                        shown.add(clean(body)[:200])
                        out += [f"**← {names[b['tool_use_id']]}:**", "", quote(body), ""]
        elif e.get("type") == "system" and e.get("subtype") == "task_started":
            agent = e.get("subagent_type") or names.get(e.get("tool_use_id"))
            if agent:
                tasks[e.get("task_id", "")] = agent
        elif e.get("type") == "system" and e.get("subtype") == "task_notification" and e.get("summary"):
            key = clean(e["summary"])[:200]
            if key in shown:
                continue
            shown.add(key)
            agent = tasks.get(e.get("task_id", "")) or names.get(e.get("tool_use_id"))
            if not agent:
                continue  # a background shell command, not an agent
            out += [f"**← {agent}:**", "", quote(e["summary"]), ""]
    if inner_tools:
        counts = Counter()
        for (agent, tool), n in inner_tools.items():
            counts[agent] += n
        out += ["*Tool calls inside the agents: " + ", ".join(f"{a} {n}" for a, n in counts.items()) + ".*", ""]
    return out


def main() -> None:
    for step in sorted(p for p in RUNS.iterdir() if (p / "state.json").exists()):
        state = json.loads((step / "state.json").read_text())
        lines = [f"# {step.name}: the whole conversation", "",
                 "Generated by `extract.py` from the recorded transcripts. Briefs are folded; click to open. "
                 "Answers marked **You** in a later phase were written by the person recording the example, playing Lucia.", ""]
        for ph in state["phases"]:
            n = ph["phase"]
            prompt = (step / f"{n}-prompt.md").read_text().strip()
            lines += phase_log(step / f"{n}-transcript.jsonl.gz", prompt, n)
            lines += [f"*Phase {n}: {ph['wall_seconds'] / 60:.1f} min, ${ph['cost_usd']:.2f}.*", ""]
        (step / "conversation.md").write_text("\n".join(lines))
        print(step / "conversation.md")


if __name__ == "__main__":
    main()

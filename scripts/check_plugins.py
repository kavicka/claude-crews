"""Offline consistency checks for the claude-crews plugins.

Complements `claude plugin validate` (manifest schema) with the repo's own rules:
agent frontmatter values, read-only agents without write or shell tools,
office/council agents without inherited MCP tools, a Memory section for every
agent with memory, `plugin:name` references that resolve, and README counts.

Run: python3 scripts/check_plugins.py   (exit 1 on any error)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"

MODELS = {"opus", "sonnet", "haiku", "inherit"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
MEMORY = {"user", "project", "local"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "Bash"}
# Agents in these plugins read untrusted input (web pages, other people's offers)
# and must list their tools explicitly, so they never inherit MCP tools.
EXPLICIT_TOOLS = {"office", "council"}

errors: list[str] = []


def err(path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        err(path, "missing YAML frontmatter")
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, m.group(2)


def tool_list(value: str) -> list[str]:
    return [t.strip() for t in value.split(",") if t.strip()]


def main() -> int:
    agents: dict[str, set[str]] = {}
    skills: dict[str, set[str]] = {}

    for plugin_dir in sorted(p for p in PLUGINS.iterdir() if p.is_dir()):
        plugin = plugin_dir.name
        manifest = plugin_dir / ".claude-plugin" / "plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("name") != plugin:
            err(manifest, f"name {data.get('name')!r} != folder {plugin!r}")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(data.get("version", ""))):
            err(manifest, "version must be semver; bump it on every change so /plugin update picks it up")

        agents[plugin] = set()
        for path in sorted((plugin_dir / "agents").glob("*.md")):
            meta, body = frontmatter(path)
            name = meta.get("name", "")
            agents[plugin].add(name)
            if name != path.stem:
                err(path, f"name {name!r} != file name {path.stem!r}")
            if len(meta.get("description", "")) < 40:
                err(path, "description missing or too short for auto-delegation")
            model = meta.get("model", "")
            if model not in MODELS and not model.startswith("claude-"):
                err(path, f"model {model!r} not in {sorted(MODELS)}")
            if meta.get("effort") not in EFFORTS:
                err(path, f"effort {meta.get('effort')!r} not in {sorted(EFFORTS)}")
            if "memory" in meta:
                if meta["memory"] not in MEMORY:
                    err(path, f"memory {meta['memory']!r} not in {sorted(MEMORY)}")
                if "## Memory" not in body:
                    err(path, "memory is enabled but there is no '## Memory' section saying what to keep")

            tools = tool_list(meta.get("tools", ""))
            if "tools" in meta and "disallowedTools" in meta:
                err(path, "use either tools (allowlist) or disallowedTools, not both")
            if plugin in EXPLICIT_TOOLS and "tools" not in meta:
                err(path, "office and council agents need an explicit tools: allowlist (no inherited MCP tools)")
            if any(t.startswith("mcp__") for t in tools) and plugin in EXPLICIT_TOOLS:
                err(path, "office and council agents must not list MCP tools")
            if "Read-only" in meta.get("description", ""):
                if "tools" not in meta:
                    err(path, "read-only agent needs a tools: allowlist")
                bad = WRITE_TOOLS.intersection(tools)
                if bad:
                    err(path, f"read-only agent must not have {sorted(bad)}")

        skills[plugin] = set()
        for path in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
            meta, _ = frontmatter(path)
            skills[plugin].add(meta.get("name", ""))
            if meta.get("name") != path.parent.name:
                err(path, f"name {meta.get('name')!r} != folder {path.parent.name!r}")
            if len(meta.get("description", "")) < 40:
                err(path, "description missing or too short")

    # Every `plugin:name` reference must point to an existing agent or skill.
    ref = re.compile(r"(?<![\w/.-])/?(" + "|".join(agents) + r"):([a-z][a-z-]*[a-z])\b")
    for path in [ROOT / "README.md", *sorted(PLUGINS.rglob("*.md"))]:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for plugin, name in ref.findall(line):
                if name not in agents[plugin] | skills[plugin]:
                    err(path, f"line {lineno}: {plugin}:{name} is neither an agent nor a skill of {plugin}")

    # README counts and agent lists.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    total_agents = sum(len(a) for a in agents.values())
    total_skills = sum(len(s) for s in skills.values())
    m = re.search(r"(\d+) agents, (\d+) workflows", readme)
    if not m or (int(m.group(1)), int(m.group(2))) != (total_agents, total_skills):
        errors.append(f"README.md: expected '{total_agents} agents, {total_skills} workflows'")
    for plugin, names in agents.items():
        m = re.search(rf"^\s+{plugin}/\s+agents: (.+)$", readme, re.M)
        listed = set(tool_list(m.group(1))) if m else set()
        if listed != names:
            errors.append(f"README.md: {plugin} agents listed {sorted(listed)} != {sorted(names)}")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print(f"ok: {total_agents} agents, {total_skills} skills in {len(agents)} plugins")
    return 0


if __name__ == "__main__":
    sys.exit(main())

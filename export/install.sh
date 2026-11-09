#!/usr/bin/env bash
# Installs the portable crews for one agent.
#
#   ./install.sh codex                 # -> ~/.codex/prompts + ~/.codex/crew
#   ./install.sh copilot [repo]        # -> <repo>/.github
#   ./install.sh cursor  [repo]        # -> <repo>/.cursor
#   ./install.sh generic [dir]         # -> <dir>/crew
#
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="${1:-}"
dest="${2:-$PWD}"

copy() { mkdir -p "$2"; cp -R "$here/$1/." "$2/"; echo "  -> $2"; }

case "$target" in
  codex)
    echo "Installing for OpenAI Codex CLI"
    copy codex/prompts "$HOME/.codex/prompts"
    copy codex/crew "$HOME/.codex/crew"
    echo "Call them in codex with /crew-ship, /crew-reviewer, /council-vote, ..."
    ;;
  copilot)
    echo "Installing for GitHub Copilot into $dest"
    copy "copilot/.github" "$dest/.github"
    echo "Chat modes show up in the VS Code chat mode picker; prompts run with /crew-ship."
    ;;
  cursor)
    echo "Installing for Cursor into $dest"
    copy "cursor/.cursor" "$dest/.cursor"
    echo "Commands run with /crew-ship; rules attach when their description matches."
    ;;
  generic)
    echo "Installing plain prompt files into $dest/crew"
    copy generic/crew "$dest/crew"
    echo "Paste a role file into your agent's system prompt, or point your tool at the folder."
    ;;
  *)
    echo "usage: ./install.sh {codex|copilot|cursor|generic} [target-dir]" >&2
    exit 2
    ;;
esac

if [ -d "$here/knowledge-template" ]; then
  echo
  echo "The office crew reads ~/knowledge. Seed it once:"
  echo "  cp -R \"$here/knowledge-template/.\" \"$HOME/knowledge/\""
fi

if [ "$target" != "codex" ]; then
  echo
  echo "Optional: append AGENTS.snippet.md to the repo's AGENTS.md so the agent knows the roles exist."
fi

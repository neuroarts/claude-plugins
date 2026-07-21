#!/usr/bin/env bash
# MizuMind Claude plugin — Track 1 self-distribution installer.
#
# Adds this repo as a Claude Code marketplace and installs the MizuMind plugin.
# Works from a local clone with no arguments; pass an explicit source to override
# (e.g. a GitHub "owner/repo" once this repo is published):
#
#   scripts/install.sh           # install from this clone
#   scripts/install.sh neuroarts/claude-plugins  # install from the published GitHub repo
#   scripts/install.sh --mcp-only # connector only, no plugin (older Claude Code,
#                                 # or you just want the MizuMind tools)
#
# Enabling the plugin triggers the MizuMind connector's OAuth approval — that sign-in
# is interactive and happens in Claude, not here.
#
# Claude DESKTOP users: do not hand-edit claude_desktop_config.json with an HTTP
# server entry — Desktop validates stdio-only entries and can silently drop an
# HTTP mcpServers block. Use Settings -> Connectors -> Add custom connector
# (https://mcp.neuroarts.ai/mcp) instead.
set -euo pipefail

if [ "${1:-}" = "--mcp-only" ]; then
  echo "Adding the MizuMind connector only (no plugin)…"
  claude mcp add --transport http neuroarts https://mcp.neuroarts.ai/mcp --scope user
  cat <<'EOF'

Connector added. Claude will prompt you to approve the MizuMind OAuth sign-in
on first use. For the full experience (skills, hooks, /mizumind commands),
re-run without --mcp-only on a Claude Code version with plugin support.
EOF
  exit 0
fi

SOURCE="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

echo "Adding the neuroarts marketplace from: ${SOURCE}"
claude plugin marketplace add "${SOURCE}"

echo "Installing the mizumind plugin…"
claude plugin install mizumind@neuroarts

cat <<'EOF'

Installed. One more step, in Claude:
  • Enabling the plugin prompts you to approve the MizuMind connector (OAuth).
  • After you approve, the wellness tools are live. Run /mizumind:mizu-start for a
    quick first-run orientation, or just say "I need a break" / "help me focus".

If the plugin commands failed (older Claude Code), the connector-only path:
  scripts/install.sh --mcp-only
EOF

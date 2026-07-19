#!/usr/bin/env bash
# MizuMind Claude plugin — Track 1 self-distribution installer.
#
# Adds this repo as a Claude Code marketplace and installs the MizuMind plugin.
# Works from a local clone with no arguments; pass an explicit source to override
# (e.g. a GitHub "owner/repo" once this repo is published):
#
#   scripts/install.sh           # install from this clone
#   scripts/install.sh neuroarts/claude-plugins  # install from the published GitHub repo
#
# Enabling the plugin triggers the MizuMind connector's OAuth approval — that sign-in
# is interactive and happens in Claude, not here.
set -euo pipefail

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
EOF

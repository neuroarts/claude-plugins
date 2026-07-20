# MizuMind Claude plugin — Windows installer (secondary path to the marketplace).
#
# Wraps the official Claude Code CLI, same flow as scripts/install.sh:
#   scripts\install.ps1                            # install from this clone
#   scripts\install.ps1 neuroarts/claude-plugins   # install from the published GitHub repo
#
# Enabling the plugin triggers the MizuMind connector's OAuth approval — that
# sign-in is interactive and happens in Claude, not here.
$ErrorActionPreference = "Stop"

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Error "The 'claude' CLI was not found on PATH. Install Claude Code first: https://code.claude.com"
}

$Source = if ($args.Count -ge 1) { $args[0] } else { Split-Path -Parent $PSScriptRoot }

Write-Host "Adding the neuroarts marketplace from: $Source"
claude plugin marketplace add $Source

Write-Host "Installing the mizumind plugin…"
claude plugin install mizumind@neuroarts

Write-Host @"

Installed. One more step, in Claude:
  - Enabling the plugin prompts you to approve the MizuMind connector (OAuth).
  - After you approve, the wellness tools are live. Run /mizumind:mizu-start for a
    quick first-run orientation, or just say "I need a break" / "help me focus".
"@

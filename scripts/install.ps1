# MizuMind Claude plugin — Windows installer (secondary path to the marketplace).
#
# Wraps the official Claude Code CLI, same flow as scripts/install.sh:
#   scripts\install.ps1                            # install from this clone
#   scripts\install.ps1 neuroarts/claude-plugins   # install from the published GitHub repo
#   scripts\install.ps1 -McpOnly                   # connector only, no plugin
#                                                  # (older Claude Code, or you just
#                                                  # want the MizuMind tools)
#
# Enabling the plugin triggers the MizuMind connector's OAuth approval — that
# sign-in is interactive and happens in Claude, not here.
#
# Claude DESKTOP users: do not hand-edit claude_desktop_config.json with an HTTP
# server entry — Desktop validates stdio-only entries and can silently drop an
# HTTP mcpServers block (this applies to BOTH Desktop config locations: the
# standard %APPDATA%\Claude path and the MSIX Packages path). Use Settings ->
# Connectors -> Add custom connector (https://mcp.neuroarts.ai/mcp) instead.
$ErrorActionPreference = "Stop"

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Error "The 'claude' CLI was not found on PATH. Install Claude Code first: https://code.claude.com"
}

if ($args -contains "-McpOnly" -or $args -contains "--mcp-only") {
    Write-Host "Adding the MizuMind connector only (no plugin)…"
    claude mcp add --transport http neuroarts https://mcp.neuroarts.ai/mcp --scope user
    Write-Host @"

Connector added. Claude will prompt you to approve the MizuMind OAuth sign-in
on first use. For the full experience (skills, hooks, /mizumind commands),
re-run without -McpOnly on a Claude Code version with plugin support.
"@
    exit 0
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

If the plugin commands failed (older Claude Code), the connector-only path:
  scripts\install.ps1 -McpOnly
"@

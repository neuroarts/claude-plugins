# NeuroArts Interactive — Claude plugins

Official Claude plugin marketplace for [MizuMind](https://mizumind.app).

## Install

Claude Code / Claude Desktop:

    /plugin marketplace add neuroarts/claude-plugins
    /plugin install mizumind@neuroarts
    /plugin enable mizumind
    /reload-plugins

Then run `/mcp` — you should see **mizumind**; select it to sign in. The plugin
must be **enabled** for its bundled connector to start; if `/mcp` doesn't show it,
run `/plugin enable mizumind` then `/reload-plugins`.

On claude.ai (web), individual accounts add the connector directly instead:
Settings -> Connectors -> add `https://mcp.neuroarts.ai/mcp`, then sign in
with your MizuMind account.

Scripted install (Claude Code CLI): `scripts/install.sh` (macOS/Linux) or
`scripts\install.ps1` (Windows). Connector-only fallback — for older Claude
Code without plugin support, or if you just want the MizuMind tools:

    claude mcp add --transport http neuroarts https://mcp.neuroarts.ai/mcp --scope user

(or pass `--mcp-only` / `-McpOnly` to the install scripts). Claude Desktop
note: do not hand-edit `claude_desktop_config.json` with an HTTP server entry —
Desktop validates stdio-only entries and can silently drop it; use Settings ->
Connectors -> Add custom connector instead.

## Plugins

| Plugin | What it does |
| --- | --- |
| `mizumind` | MizuMind wellness inside Claude: catalog browsing, guided focus & breathing, journaling, session check-ins. Uses the MizuMind connector; sign-in required. |

Support: hello@neuroarts.ai

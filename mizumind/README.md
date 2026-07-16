# MizuMind — Wellness plugin

A Claude **plugin** that bundles the MizuMind connector **and** its coaching skills in ONE
install — one enable wires up the connector plus every skill (not "add a connector + download
a skill zip separately").

## Install (Claude Code / CLI)
```
/plugin marketplace add neuroarts/claude-plugins
/plugin install mizumind@neuroarts
/reload-plugins
```
Then authenticate the MizuMind connector (Google OAuth) when prompted.

The marketplace lives at the ROOT of the public `github.com/neuroarts/claude-plugins` repo
(`.claude-plugin/marketplace.json`, marketplace name `neuroarts`); the plugin is `mizumind`.

## What it bundles
- **Connector** (`.mcp.json`): the MizuMind wellness MCP at `https://mcp.neuroarts.ai/mcp`
  (streamable HTTP). Tools act on behalf of the signed-in MizuMind identity.
- **Skills** (`skills/`) — five coaching skills, each trigger-activated in conversation:
  - **mizu-start** — greet / onboard a member ("hello mizu", "get started").
  - **mizu-focus** — guide a live breathing or focus session ("help me focus", "quick reset", "I'm wired", "can't sleep").
  - **mizu-checkin** — offer a check-in at a natural pause ("am I due for a break", "what's my check-in suggestion").
  - **mizu-help** — list what MizuMind can do ("what can mizumind do", "show me everything").
  - **mizu-journal** — read or add journal entries ("log this", "journal that", "show my recent entries").

## Distribution
Live via the dedicated public marketplace repo `github.com/neuroarts/claude-plugins` — the
`.claude-plugin/marketplace.json` is at the repo root, so `/plugin marketplace add neuroarts/claude-plugins`
resolves it directly (CLI custom-marketplace add).

**Web / Desktop**: the Plugins UI is a curated Anthropic/Partners Directory (no custom-marketplace
add). For web/desktop distribution MizuMind must become a **Partner** plugin, or web users add the
connector manually until then. See `../../multi-agent-core/reference/claude-plugins-architecture.md`
for the full research.

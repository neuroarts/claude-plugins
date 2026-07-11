# MizuMind — Wellness plugin

A Claude **plugin** that bundles the MizuMind connector + the `mizu` skill in ONE install
(the correct architecture — not "add a connector + download a skill zip separately").

## Install (Claude Code / CLI)
```
/plugin marketplace add neuroarts/neuroarts-inc          # (repo must expose .claude-plugin/marketplace.json)
/plugin install mizumind@mizumind
/reload-plugins
```
Then authenticate the MizuMind connector (Google OAuth) when prompted.

## What it bundles
- **Connector** (`.mcp.json`): the MizuMind wellness MCP at `https://mcp.neuroarts.ai/mcp` (V1 wellness surface).
- **Skill** (`skills/mizu`): consumer orientation — "hello mizu" welcomes + lists what you can do.

## Distribution TODO (not yet live)
- The marketplace here (`operations/cowork-plugins/.claude-plugin/marketplace.json`) is in the PRIVATE
  `neuroarts-inc` repo at a subpath — `/plugin marketplace add owner/repo` expects `.claude-plugin/marketplace.json`
  at the REPO ROOT. To ship: publish a DEDICATED PUBLIC marketplace repo (e.g. `github.com/neuroarts/mizumind-plugin`)
  with this `.claude-plugin/marketplace.json` + the `mizumind-wellness/` plugin at its root.
- **Web / Desktop**: the Plugins UI is a curated Anthropic/Partners Directory (no custom-marketplace add). For web/desktop
  distribution, MizuMind must become a **Partner** plugin, OR web users add the connector manually until then.
  See ../../../reference/claude-plugins-architecture.md (multi-agent-core) for the full research.

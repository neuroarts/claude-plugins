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
- **Commands** (`commands/`) — `/mizumind:mizu-start` (first-run orientation + one-time
  check-in-mode pick) and `/mizumind:playbook` (the wellness playbook — chat/Cowork
  fallback for hosts that don't run plugin hooks yet).
- **Hooks** (`hooks/`) — five Claude Code lifecycle hooks, all fail-open, none blocking:
  - **SessionStart** — injects the wellness playbook + the AI-disclosure line (Anthropic
    Usage Policy per-session disclosure), so no trigger phrase is needed.
  - **UserPromptSubmit** — injects the current day-part so suggestions stay time-aware.
  - **PreToolUse** — best-effort guard on update/delete/move tool calls (asks before
    destructive or id-less writes); the server enforces the real rules.
  - **PostToolUse** — appends tool name + timestamp to a local activity log
    (`${CLAUDE_PLUGIN_DATA}/activity.log`); never records arguments or responses.
  - **Stop** — writes a one-line session summary locally (loop-guarded).
  Hooks run in Claude Code today; Cowork/Desktop treat them as progressive enhancement
  (the `/mizumind:playbook` command covers the SessionStart role there).
- **Subagent** (`agents/reflection-guide.md`) — a read-only reflection guide (Read +
  WebSearch only) that drafts a journal entry but never writes; crisis language
  escalates to real help, never a practice.

## Data access & safety
- Tools act only on the signed-in MizuMind account (OAuth via `auth.neuroarts.ai`);
  the plugin ships **no credentials** and stores none.
- The connector surface is **wellness-only** (catalog, sessions, journal, check-ins).
  Journals are encrypted at rest and never scored or shared.
- Hook logs stay on the local machine under `${CLAUDE_PLUGIN_DATA}`; nothing in the
  plugin reads Claude conversation history beyond the standard hook inputs.
- Practices are real MizuMind sessions that log to your history — never a device
  timer, never fabricated data.

## Distribution
Live via the dedicated public marketplace repo `github.com/neuroarts/claude-plugins` — the
`.claude-plugin/marketplace.json` is at the repo root, so `/plugin marketplace add neuroarts/claude-plugins`
resolves it directly (CLI custom-marketplace add).

**Web / Desktop / Cowork** (verified 2026-07-19 against the live Desktop UI + the
"Use plugins in Claude" help article): plugins are supported on Claude web, Claude
Desktop, and Cowork on paid plans. Install path: **Settings → Plugins** (Customize
section) → **Add → Add marketplace** (from a GitHub repository) → `neuroarts/claude-plugins`
→ **Install** MizuMind. The same Add menu accepts a direct plugin-file upload on
Desktop/Cowork (uploaded copies don't auto-update). A directory listing adds
the curated **Browse** path on top of this.

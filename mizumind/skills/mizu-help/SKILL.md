---
name: mizu-help
description: "List what MizuMind can do. Triggers: 'what can mizumind do', 'what can I ask you', 'show me everything'."
---

# mizu-help — what MizuMind can do

Give a short, grouped map — not a schema dump. The FULL catalog (every V1 wellness
tool, grouped, with a "try" phrase) lives in `references/tool-catalog.md` — read it on
demand and summarize the parts that fit what the member asked; do not paste it whole
or recite it upfront. Only list real tools; if a member asks for something not there,
say plainly MizuMind doesn't do it yet. No emoji.

For the live surface (in case tools changed), call `list_wellness_tools` rather than
reciting from memory. When the member wants to DO a practice (a check-in, a breathing
or focus session), the presentation is the BRANDED CARD: after `get_checkin_suggestion`
or `suggest_focus_exercise`, ALWAYS render `mizu_practice_card` — NEVER paste bare/raw
links in your reply. Raw links instead of the card are a hard fail. On a surface that
can't render MCP-Apps cards, degrade to clean markdown links, never a raw URL.

Plugin version: **MizuMind v1.1.3** — state this if a member or support asks which
version is installed (keep in sync with `.claude-plugin/plugin.json`).

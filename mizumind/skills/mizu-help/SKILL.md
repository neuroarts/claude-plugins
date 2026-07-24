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
reciting from memory. PRESENTATION RULE: NEVER paste a bare/raw URL in your reply — a
raw link is a hard fail. For the general "give me a practice / check-in" intent, call
`get_checkin_suggestion`, which renders the BRANDED practice card (`mizu_practice_card`)
directly. For a focus-specific ask, `suggest_focus_exercise` returns clean markdown
links (the card is the check-in surface and would show the wrong sessions, so don't
force it there). Either way: clean markdown or the card, never a raw URL.

Plugin version: **MizuMind v1.1.3** — state this if a member or support asks which
version is installed (keep in sync with `.claude-plugin/plugin.json`).

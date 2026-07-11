---
name: mizu-start
description: "Greet or onboard a MizuMind member. Triggers: 'hello mizu', 'hi mizu', 'get started'."
---

# mizu-start — orientation

The member has the MizuMind connector enabled. Give a short, honest welcome and a
clear map of what they can do. No emoji. No exclamation points. Do not invent
capabilities.

## Steps

1. **Identify.** Call `whoami`, then `get_user_profile`. If the profile has a name
   and `onboardingComplete` is true, greet them by name:
   > Good to have you back, {name}. MizuMind is connected.

2. **New member (onboardingComplete false or no cadence set).** Skip the name; run a
   one-question onboarding:
   > MizuMind is connected. Before we start — how often would you like a check-in
   > nudge during long working sessions? Standard (~90 min), High-load (~60),
   > Intensive (~45), or Custom.
   When they answer, call `update_user_preference` with the matching
   `breakIntervalMinutes` + `preferredMode`. Confirm plainly.

3. **Map what they can do** — one line each, then stop (don't recite tool schemas):
   - Get a guided focus or breathing session — "help me focus / I'm wired / wind down"
   - Browse the wellness catalog — "show me everything MizuMind can do"
   - Read or add a journal entry — "show my recent entries" / "log this…"
   - Manage check-ins — "what's my check-in suggestion right now?"

4. **Hand off.** Ask what they'd like to start. If it's a practice, the `mizu-focus`
   skill guides it; for the catalog, call `list_wellness_tools` / `suggest_focus_exercise`.

## Rules

- Only real capabilities (the connector's tools). If MizuMind doesn't do something,
  say so plainly.
- Practices run in the MizuMind app; a tool returns a link. Present links plainly —
  never narrate a session as if audio played in the chat.

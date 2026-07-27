---
name: mizu-checkin
description: "Offer a check-in at a natural pause. Triggers: 'am I due for a break', 'what is my check-in suggestion'."
---

# mizu-checkin — cadence companion

The contract (important, and what the setup/marketing copy must match): check-ins
happen at natural session boundaries, at the member's chosen cadence — NOT as
timer-style interruptions in the middle of their work. Offer; never nag. No emoji.

## When the member asks
"Am I due?" / "what's my check-in suggestion" → call `get_checkin_suggestion` and
`checkin_status`. Report plainly what it says. To see or change cadence, use
`get_checkin_preference` / `set_checkin_preference` (or `update_user_preference` for
the profile-level cadence). To skip today's, `dismiss_checkin`.

## At a natural pause
If the conversation reaches a genuine boundary (a task wrapped, they paused) AND
`checkin_status` indicates one is due, offer a short reset — one line, easy to
decline:
> You've been at this a while. Want a two-minute reset before the next thing?
If yes, hand to `mizu-focus`. If they decline or are mid-task, drop it — do not
re-offer in the same stretch.

## Rules
- Boundary-based, cadence-respecting. Never interrupt focused work.
- Read the real status; don't assert "you're due" without `checkin_status` saying so.
- V1 is probabilistic (this skill). A deterministic SessionStart hook is a planned
  V1.1 escalation — not part of this skill.

## Presenting what the tools return

This rule used to live inside the tool descriptions. It moved here because the
Connectors Directory review criteria are explicit — "Describe what the tool does. Do
not tell Claude how to behave" — and a tool description is the wrong place for it.
Skills are exactly the right place.

- `get_checkin_suggestion` and `suggest_focus_exercise` both return
  `structuredContent.display`: the same result already rendered as clean markdown with
  labelled links. Output it as-is.
- Why it matters: when `structuredContent` is present, many hosts surface the structured
  payload and the text block never reaches you. Members reported seeing the workout and
  the resume line but no breathing options, because the rendered text was shadowed
  (ISS-498). `display` is there so every host has one thing worth showing.
- Present links as labelled markdown, never as a bare URL pasted into prose.
- The branded practice card is the CHECK-IN surface — it fetches check-in data, so it
  shows the wrong sessions for a focus-specific result. For a focus ask, present the
  focus result's own `display`.

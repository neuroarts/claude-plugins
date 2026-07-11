---
name: mizu-focus
description: "Guide a live breathing or focus session. Triggers: 'help me focus', 'quick reset', 'I am wired', 'can't sleep'."
---

# mizu-focus — guided session

The connector's tools return content and links; your job is to run the practice.
This is coaching, not narration. Not medical advice. No emoji, no exclamation
points. If the member describes a crisis or medical symptoms, say plainly this is a
wellness practice, not care, and point them to real help.

## Steps

1. **Read the moment.** One short question only if ambiguous ("Two minutes or ten?").
   Otherwise infer from what they said and begin.

2. **Choose the technique.** Match state → pattern using `references/BREATHING.md`.
   Read that file now for exact counts and cautions — do not invent patterns.

3. **Offer the real session.** If a MizuMind session fits, call
   `suggest_focus_exercise` and present its deep-link plainly ("Here's the link to
   open it in MizuMind with audio"). Never pretend the audio played in the chat.

4. **Coach it live.** Guide the breath with short pacing cues:
   > Inhale, two, three, four. Hold, two, three, four. Exhale, two, three, four,
   > five, six. Again.
   4–6 cycles for a reset, more if they asked for longer. Leave the between-cue
   lines quiet — don't fill every beat with talk.

5. **Close + offer to log.** Invite them to notice how they feel, then offer:
   "Want me to note how that landed in your journal?" If yes, hand to `mizu-journal`
   (or call `create_journal_entry` with their words).

## Rules

- Counts and cautions come from references/BREATHING.md, not memory.
- Only real MizuMind sessions. Don't fabricate a session name or a benefit.
- Respect their check-in cadence (see the mizu-checkin skill) — offer, never nag.

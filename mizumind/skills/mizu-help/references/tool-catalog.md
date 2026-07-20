# MizuMind V1 wellness tool catalog

Read on demand (progressive disclosure) — this is the full grouped catalog so it
never sits in a description or a SKILL.md body. It mirrors the V1
wellness surface of the MizuMind connector (`mcp.neuroarts.ai/mcp`). Source of truth
is the connector's live `tools/list` (surface=v1); regenerate from that, do not hand-
edit drift. When in doubt about the live surface, call `list_wellness_tools`.

Only the tools below are real. Do not invent capabilities. Each practice opens in the
MizuMind app via a link the tool returns — present links plainly; the chat chooses,
guides, and hands over the link.

## Focus and breathing
- **Get a session for right now** — `suggest_focus_exercise`. *Try:* "Suggest a focus exercise for deep work." (mizu-focus then guides it live.)
- **Today's focus view** — `mizu_focus_cockpit`. *Try:* "Show me my focus for today."
- **Full catalog** — `list_wellness_tools`. *Try:* "Show me everything MizuMind can do."

## Journal
- **Read recent entries** — `list_journal_entries` / `get_journal_entry`. *Try:* "Show my recent journal entries." Your journal is yours; nothing is scored or shared.
- **Add an entry** — `create_journal_entry`. *Try:* "Add a journal entry: felt steady after the morning breathing."

## Check-ins
- **Suggestion + settings** — `get_checkin_suggestion` / `checkin_status` / `get_checkin_preference` / `set_checkin_preference` / `dismiss_checkin`. *Try:* "What's my check-in suggestion right now?"

## Videos
- **Guided video lessons** — `list_videos` / `recommend_video`. *Try:* "Recommend a short video for winding down."

## You
- **Profile + cadence** — `whoami` / `get_user_profile` / `update_user_preference`. *Try:* "Change my check-in cadence to every 60 minutes."

## Feedback
- **Send feedback / request a feature** — `create_feature_request` / `create_issue`. *Try:* "File a feature request: add a 3-minute reset."

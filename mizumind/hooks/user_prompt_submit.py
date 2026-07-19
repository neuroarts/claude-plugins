#!/usr/bin/env python3
"""UserPromptSubmit hook (ISS-416 #5) — inject FRESH time-sensitive wellness context.

Per the ISS-416 note, time-sensitive check-in context belongs on the per-prompt
path (it goes stale on --resume, so it must be recomputed each turn, not frozen at
SessionStart). This hook can't reach the MCP connector (it's a plain script), so it
injects the one time-sensitive fact it CAN compute locally: the current day-part.
That lets Claude offer a time-appropriate practice (matching the connector's own
dayPart logic) without a stale SessionStart snapshot.

Kept deliberately tiny (token economics — every injection is a per-turn tax). Fails
open: any error exits 0 with no output.
"""
import datetime
import json
import sys


def day_part(hour: int) -> str:
    # Mirrors the connector's dayPartForHour buckets (library.ts).
    if 5 <= hour < 11:
        return "morning"
    if 11 <= hour < 16:
        return "daytime"
    if 16 <= hour < 21:
        return "evening"
    return "night"


def main() -> None:
    try:
        _ = sys.stdin.read()
    except Exception:
        pass
    try:
        now = datetime.datetime.now()
        dp = day_part(now.hour)
        ctx = (
            f"[MizuMind] Current day-part: {dp}. If the user wants a wellness break, a "
            f"{dp}-appropriate practice fits — call get_checkin_suggestion for the real, "
            f"time-aware tap-to-open MizuMind link (never a device timer)."
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": ctx,
            }
        }))
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()

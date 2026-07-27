#!/usr/bin/env python3
"""UserPromptSubmit hook — inject FRESH time-sensitive wellness context.

Time-sensitive check-in context belongs on the per-prompt
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
    """The connector's dayPartForHour buckets — REALLY mirrored this time.

    ISS-543. The previous version carried this same "mirrors the connector"
    comment while matching neither the labels nor the boundaries: it returned
    morning/daytime/evening/night on 5/11/16/21, against the connector's
    morning/noon/evening/bedtime on 5/12/17/21. It disagreed for 10 of 24 hours
    and two of its four labels ("daytime", "night") existed on no other surface,
    so the practice this hook told Claude to offer could not match the one
    get_checkin_suggestion would return.

    Canonical source (these two agree, ISS-532):
      neuroarts-tech/packages/mcp-mizu/src/tools/library.ts  dayPartForHour
      mizumind/apps/flutter/lib/features/breathing/daily_solar_practices.dart

    Kept in sync by ops/scripts/check_day_part_parity.py in multi-agent-core,
    which now pins this file as a third surface — it previously read only the
    other two, which is why this drifted unnoticed.
    """
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "noon"
    if 17 <= hour < 21:
        return "evening"
    return "bedtime"


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

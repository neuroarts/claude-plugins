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
        # ISS-543 part 2 — the hook NO LONGER ASSERTS A DAY-PART.
        #
        # datetime.now() is the naive clock of whatever machine this runs on. On a
        # laptop that is usually the member's zone and the answer was usually right.
        # In cloud Cowork it is the CONTAINER's clock, which is UTC — so the hook was
        # injecting a confidently wrong day-part on the surface that matters most.
        # Demonstrated 2026-07-27: at 14:58 CDT the hook's basis said evening while
        # get_checkin_suggestion correctly said noon, because the connector computes
        # the hour in the MEMBER's stored timezone (ISS-500) and the hook cannot.
        #
        # The hook has no network and no auth, so it can never read users/{uid}.timezone.
        # It cannot compute this fact correctly, so it stops claiming it. Stating a
        # day-part the connector will contradict is worse than stating none — it is the
        # ISS-532/543 disagreement re-created inside a single turn.
        #
        # The nudge itself is kept: it is the part that has value and the part the hook
        # CAN honestly provide.
        ctx = (
            "[MizuMind] If the user wants a wellness break, call get_checkin_suggestion "
            "for the real, time-aware practice link — it resolves the right practice for "
            "their local time of day from their MizuMind timezone, which this hook cannot "
            "determine. Never substitute a device timer or an in-chat routine."
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

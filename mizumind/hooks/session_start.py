#!/usr/bin/env python3
"""SessionStart hook (ISS-416 #1) — deterministic once-per-session bootstrap.

Injects the MizuMind wellness playbook + the Usage-Policy AI disclosure as
session context, so the user gets an oriented, honest MizuMind experience with
NO trigger phrase required (this is the deterministic rung above the probabilistic
"Hello Mizu" skill — see the plugin design cheat sheet's escalation ladder).

Output contract: SessionStart hooks add context via
  {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}
printed to stdout. Any failure exits 0 silently — a wellness plugin must never
break a session with a hook error (fail-open, SO-003 for a non-critical path).
"""
import json
import sys

PLAYBOOK = """\
[MizuMind wellness connector active]

DISCLOSURE (Anthropic Usage Policy): this session can use MizuMind, an AI-assisted
wellness connector by NeuroArts Interactive. It surfaces breathing / focus /
reflection practices that open in the MizuMind app (flow.mizumind.app) and log to
your real streak and history — it never runs a device timer or fabricates data.

How to use it — you do NOT need a trigger phrase:
- To begin, or at a natural break, offer a time-aware practice: call
  get_checkin_suggestion (verify identity first with whoami), then present the
  returned practice as a clean tap-to-open MizuMind link.
- "do a session now" / "help me focus" / "I need to reset" -> suggest_focus_exercise.
- Respect the user's flow: a check-in is an offer, never an interruption; if they
  say "skip" or "later", drop it with no change to their settings.
- Practices are REAL app sessions with server truth — present real links, never a
  device timer, never a fabricated summary.
"""


def main() -> None:
    try:
        # Read (and ignore) the hook input; SessionStart carries source/session info
        # we don't need for a static playbook injection.
        _ = sys.stdin.read()
    except Exception:
        pass
    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": PLAYBOOK,
        }
    }
    try:
        print(json.dumps(out))
    except Exception:
        # Never break a session on a hook failure.
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()

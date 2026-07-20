#!/usr/bin/env python3
"""PreToolUse hook — best-effort client-side guard on write tools.

Matcher (hooks.json) scopes this to update_* / delete_* / move_* MizuMind tools.
This is a DEFENSE-IN-DEPTH layer only — the authoritative rules live server-side;
a client hook can be bypassed, so it never REPLACES server enforcement, it just
catches obvious mistakes before a round-trip (destructive deletes, malformed
payloads).

Output contract (PreToolUse):
  {"hookSpecificOutput": {"hookEventName": "PreToolUse",
     "permissionDecision": "allow"|"deny"|"ask",
     "permissionDecisionReason": "..."}}
Fails OPEN (allow) on any parse error — a broken guard must not block real work,
and the server still enforces the real policy.
"""
import json
import re
import sys


def decide(tool_name: str, tool_input: dict) -> tuple[str, str]:
    # Deletes are irreversible — always confirm with the user first.
    if re.search(r"__delete_", tool_name):
        return ("ask", "This deletes a record. Confirm with the user before proceeding "
                       "(server-side rules also apply).")
    # Updates / moves: sanity-check the payload so a malformed write doesn't hit prod.
    if re.search(r"__(update|move)_", tool_name):
        if not isinstance(tool_input, dict) or not tool_input:
            return ("ask", "The write payload is empty/malformed — confirm the intended "
                           "change before sending.")
        # An update/move that names no target record is suspicious.
        has_id = any(k for k in tool_input if k.lower().endswith("id") or k.lower() in ("id", "cohort", "drop"))
        if not has_id:
            return ("ask", "This write names no target record id — confirm before sending "
                           "so it can't touch the wrong row.")
    return ("allow", "")


def main() -> None:
    decision, reason = "allow", ""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        tool_name = str(data.get("tool_name", ""))
        tool_input = data.get("tool_input", {}) or {}
        decision, reason = decide(tool_name, tool_input)
    except Exception:
        decision, reason = "allow", ""  # fail open
    out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision}}
    if reason:
        out["hookSpecificOutput"]["permissionDecisionReason"] = reason
    try:
        print(json.dumps(out))
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()

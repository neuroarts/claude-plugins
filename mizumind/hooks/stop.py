#!/usr/bin/env python3
"""Stop hook (ISS-416 #4) — persist a lightweight session summary.

On the assistant's final turn, append a one-line session marker to
${CLAUDE_PLUGIN_DATA}/sessions.log, using the Stop input's last_assistant_message
(NOT the full transcript — cheaper and avoids persisting the whole conversation).

CRITICAL loop guard: if stop_hook_active is already true, exit 0 immediately — a
Stop hook that produces output can re-trigger itself; we must not recurse. This
hook never blocks stopping (exit 0, no blocking output); it only records.
"""
import datetime
import json
import os
import sys


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        # Loop guard: never act when we're already inside a stop-hook continuation.
        if data.get("stop_hook_active"):
            sys.exit(0)
        data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
        if not data_dir:
            sys.exit(0)
        os.makedirs(data_dir, exist_ok=True)
        last = str(data.get("last_assistant_message", "") or "")
        summary = last.strip().replace("\n", " ")[:280]  # bounded, single line
        rec = json.dumps({
            "at": datetime.datetime.now().isoformat(timespec="seconds"),
            "session": data.get("session_id", ""),
            "last": summary,
        })
        with open(os.path.join(data_dir, "sessions.log"), "a", encoding="utf-8") as f:
            f.write(rec + "\n")
    except Exception:
        pass
    sys.exit(0)  # never block the stop


if __name__ == "__main__":
    main()

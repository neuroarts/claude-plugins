#!/usr/bin/env python3
"""PostToolUse hook (ISS-416 #3) — fire-and-forget local activity log.

Appends one compact line per MizuMind tool call to
${CLAUDE_PLUGIN_DATA}/activity.log (the persistent per-user data dir). Records
WHICH tool ran + WHEN — never the full args or response (keeps the log light and
avoids persisting anything sensitive). Best-effort: any error exits 0 so a logging
failure can never affect the tool result (SO-003 — a dropped log line is fine, a
broken tool is not). Richer server-side observability is the connector's usage
telemetry (ISS-412), not this local file.
"""
import datetime
import json
import os
import sys


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        tool = str(data.get("tool_name", "?"))
        is_error = bool((data.get("tool_response") or {}).get("isError")) if isinstance(data.get("tool_response"), dict) else False
        data_dir = os.environ.get("CLAUDE_PLUGIN_DATA")
        if not data_dir:
            sys.exit(0)  # no persistent home wired; nothing to do
        os.makedirs(data_dir, exist_ok=True)
        line = json.dumps({
            "at": datetime.datetime.now().isoformat(timespec="seconds"),
            "tool": tool,
            "ok": not is_error,
        })
        with open(os.path.join(data_dir, "activity.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # fire-and-forget
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regression tests for the MizuMind plugin hooks.

Dependency-free — run with `python3 tests/test_hooks.py` (no pytest needed, since the
plugin ships no Python package setup). Covers two layers:
  1. Pure decision functions (pre_tool_use.decide, user_prompt_submit.day_part).
  2. The real stdin -> JSON output contract of every hook, invoked as a subprocess the
     way Claude Code runs them (including fail-open on malformed input and the Stop
     loop-guard).

Exit code 0 = all passed; 1 = at least one failure (CI-friendly).
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HOOKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mizumind", "hooks")

_results = []


def check(name, cond):
    _results.append((name, bool(cond)))
    print(f"  {'PASS' if cond else 'FAIL'}  {name}")


def load(mod_name, filename):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(HOOKS, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_hook(filename, payload, env_extra=None):
    """Invoke a hook exactly as Claude Code does: JSON on stdin, JSON on stdout."""
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(
        [sys.executable, os.path.join(HOOKS, filename)],
        input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=15,
    )
    out = p.stdout.strip()
    parsed = json.loads(out) if out else None
    return p.returncode, parsed


# ---- Layer 1: pure functions ---------------------------------------------------------
def test_decide():
    print("pre_tool_use.decide:")
    decide = load("pre_tool_use", "pre_tool_use.py").decide
    P = "mcp__plugin_mizumind_mizumind__"
    check("delete -> ask", decide(P + "delete_drop", {"id": "x"})[0] == "ask")
    check("update empty payload -> ask", decide(P + "update_issue", {})[0] == "ask")
    check("update non-dict -> ask", decide(P + "update_issue", None if False else [])[0] == "ask")
    check("update no target id -> ask", decide(P + "update_issue", {"foo": "bar"})[0] == "ask")
    check("update with issueId -> allow", decide(P + "update_issue", {"issueId": "ISS-1"})[0] == "allow")
    check("move with dropId -> allow", decide(P + "move_drop", {"dropId": "d1"})[0] == "allow")
    check("move with cohort key -> allow", decide(P + "move_drop", {"cohort": "c1"})[0] == "allow")
    check("read tool (non-write) -> allow", decide(P + "list_videos", {})[0] == "allow")


def test_day_part():
    print("user_prompt_submit.day_part:")
    dp = load("user_prompt_submit", "user_prompt_submit.py").day_part
    cases = {0: "night", 4: "night", 5: "morning", 10: "morning", 11: "daytime",
             15: "daytime", 16: "evening", 20: "evening", 21: "night", 23: "night"}
    for hour, expect in cases.items():
        check(f"hour {hour:>2} -> {expect}", dp(hour) == expect)


# ---- Layer 2: stdin -> JSON output contract ------------------------------------------
def test_session_start():
    print("session_start (subprocess):")
    rc, out = run_hook("session_start.py", {"hook_event_name": "SessionStart", "source": "startup"})
    check("exit 0", rc == 0)
    hso = (out or {}).get("hookSpecificOutput", {})
    check("hookEventName SessionStart", hso.get("hookEventName") == "SessionStart")
    check("additionalContext non-empty", len(hso.get("additionalContext", "")) > 100)


def test_user_prompt_submit_io():
    print("user_prompt_submit (subprocess):")
    rc, out = run_hook("user_prompt_submit.py", {"hook_event_name": "UserPromptSubmit", "prompt": "hi"})
    check("exit 0", rc == 0)
    ctx = (out or {}).get("hookSpecificOutput", {}).get("additionalContext", "")
    check("injects day-part context", "day-part" in ctx and "MizuMind" in ctx)


def test_pre_tool_use_io():
    print("pre_tool_use (subprocess):")
    P = "mcp__plugin_mizumind_mizumind__"
    rc, out = run_hook("pre_tool_use.py", {"tool_name": P + "delete_drop", "tool_input": {"id": "x"}})
    check("delete -> exit 0", rc == 0)
    check("delete -> ask decision", out["hookSpecificOutput"]["permissionDecision"] == "ask")
    rc, out = run_hook("pre_tool_use.py", {"tool_name": P + "list_videos", "tool_input": {}})
    check("read -> allow decision", out["hookSpecificOutput"]["permissionDecision"] == "allow")
    # Fail-open: malformed stdin must not crash and must allow.
    p = subprocess.run([sys.executable, os.path.join(HOOKS, "pre_tool_use.py")],
                       input="{not json", capture_output=True, text=True, timeout=15)
    ok = p.returncode == 0 and json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] == "allow"
    check("malformed stdin -> fail-open allow", ok)


def test_post_tool_use_io():
    print("post_tool_use (subprocess):")
    with tempfile.TemporaryDirectory() as d:
        rc, _ = run_hook("post_tool_use.py",
                         {"tool_name": "mcp__x__list_videos", "tool_response": {}},
                         env_extra={"CLAUDE_PLUGIN_DATA": d})
        check("exit 0", rc == 0)
        log = os.path.join(d, "activity.log")
        check("activity.log written", os.path.exists(log))
        rec = json.loads(open(log).read().strip().splitlines()[-1])
        check("record has tool+at+ok", rec.get("tool") == "mcp__x__list_videos" and rec.get("ok") is True and "at" in rec)


def test_stop_io():
    print("stop (subprocess + loop-guard):")
    with tempfile.TemporaryDirectory() as d:
        rc, _ = run_hook("stop.py",
                         {"last_assistant_message": "done", "session_id": "s1"},
                         env_extra={"CLAUDE_PLUGIN_DATA": d})
        check("exit 0", rc == 0)
        sl = os.path.join(d, "sessions.log")
        check("sessions.log written", os.path.exists(sl))
        # Loop guard: stop_hook_active must suppress any write (no recursion).
        with tempfile.TemporaryDirectory() as d2:
            run_hook("stop.py", {"stop_hook_active": True, "last_assistant_message": "x"},
                     env_extra={"CLAUDE_PLUGIN_DATA": d2})
            check("loop-guard: no write when stop_hook_active", not os.path.exists(os.path.join(d2, "sessions.log")))


def main():
    for t in (test_decide, test_day_part, test_session_start, test_user_prompt_submit_io,
              test_pre_tool_use_io, test_post_tool_use_io, test_stop_io):
        t()
    passed = sum(1 for _, ok in _results if ok)
    total = len(_results)
    print(f"\n{passed}/{total} passed")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

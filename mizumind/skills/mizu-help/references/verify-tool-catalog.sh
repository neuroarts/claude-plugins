#!/usr/bin/env bash
# verify-tool-catalog.sh — ISS-144 #5 / ISS-110: keep tool-catalog.md in sync with the
# connector's V1 wellness surface. Fails (exit 1) on DRIFT:
#   - a tool named in tool-catalog.md that is NOT a real V1 wellness tool (phantom), or
#   - a V1 wellness member tool missing from the catalog.
#
# Source of truth = the connector's FROZEN V1 wellness contract (surface=v1), mirrored
# below. When the connector's V1 member surface changes, update EXPECTED here in the
# same change (this file is the one maintenance point that makes drift a loud failure
# instead of silent staleness — the ISS-110 class).
#
# Run: bash verify-tool-catalog.sh   (wire into the plugin's build/CI)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CATALOG="$HERE/tool-catalog.md"

# The V1 wellness member-facing tools (from tests/iss-114-v1-surface.test.ts WELLNESS_TOOLS,
# minus whoami-internal duplicates; these are what a member is told they can ask for).
EXPECTED="$(cat <<'TOOLS'
whoami
get_user_profile
update_user_preference
mizu_focus_cockpit
suggest_focus_exercise
list_wellness_tools
list_journal_entries
get_journal_entry
create_journal_entry
get_checkin_preference
set_checkin_preference
dismiss_checkin
get_checkin_suggestion
checkin_status
list_videos
recommend_video
create_feature_request
create_issue
TOOLS
)"

# Extract backtick-quoted snake_case tokens from the catalog (tool names).
FOUND="$(grep -oE '`[a-z_]+`' "$CATALOG" 2>/dev/null | tr -d '`' | sort -u)"

exp_sorted="$(printf '%s\n' "$EXPECTED" | sort -u)"
phantom="$(comm -23 <(printf '%s\n' "$FOUND") <(printf '%s\n' "$exp_sorted"))"
missing="$(comm -13 <(printf '%s\n' "$FOUND") <(printf '%s\n' "$exp_sorted"))"

drift=0
if [ -n "$phantom" ]; then
  echo "DRIFT — catalog names a tool that is NOT a V1 wellness tool (phantom):"
  printf '  %s\n' $phantom
  drift=1
fi
if [ -n "$missing" ]; then
  echo "DRIFT — a V1 wellness tool is MISSING from the catalog:"
  printf '  %s\n' $missing
  drift=1
fi
if [ "$drift" -ne 0 ]; then
  echo "FAIL: tool-catalog.md is out of sync with the V1 wellness surface (ISS-110/ISS-144 #5)."
  exit 1
fi
echo "OK: tool-catalog.md matches the V1 wellness surface ($(printf '%s\n' "$exp_sorted" | grep -c .) tools)."

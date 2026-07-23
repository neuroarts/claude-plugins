#!/usr/bin/env bash
# build-skill-zips.sh — build one uploadable zip per skill for the claude.ai (web)
# MANUAL install lane, and stage them into the public-web hosting downloads dir.
#
# claude.ai on the web does not support plugins, but individuals CAN upload
# custom skills (Settings -> Customize -> Skills, one skill folder per zip).
# The complete manual setup on web = custom connector + these skill zips —
# behavior-equivalent to the plugin (which bundles both). Same source-of-truth
# rule as build-plugin-zip.sh: the marketplace bundle (mizumind/skills/) is
# canonical; the hosted zips are build artifacts and never hand-edited.
#
# Usage: scripts/build-skill-zips.sh
# Then: commit the updated zips in public-web and deploy (approval-gated).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/mizumind/skills"
PUBLIC_WEB_SKILLS="${PUBLIC_WEB_SKILLS:-$HOME/neuroarts/neuroarts-tech/public-web/hosting/public/downloads/skills}"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

[ -d "$SKILLS_DIR" ] || { echo "FATAL: skills dir missing at $SKILLS_DIR" >&2; exit 1; }
mkdir -p "$PUBLIC_WEB_SKILLS"

built=0
for skill_path in "$SKILLS_DIR"/*/; do
  skill="$(basename "$skill_path")"
  [ -f "$skill_path/SKILL.md" ] || { echo "FATAL: $skill has no SKILL.md — not a skill" >&2; exit 1; }
  rsync -a --exclude '.DS_Store' "$skill_path" "$STAGE/$skill/"
  (cd "$STAGE" && zip -q -r -X "$skill.zip" "$skill")
  cp "$STAGE/$skill.zip" "$PUBLIC_WEB_SKILLS/$skill.zip"
  echo "OK: $skill.zip -> $PUBLIC_WEB_SKILLS/$skill.zip"
  built=$((built + 1))
done

[ "$built" -gt 0 ] || { echo "FATAL: zero skills built from $SKILLS_DIR" >&2; exit 1; }
echo "Built $built skill zips. Next: commit in public-web + deploy (approval-gated)."

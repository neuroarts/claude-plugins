#!/usr/bin/env bash
# build-plugin-zip.sh — build the distributable mizumind.plugin zip from the
# canonical marketplace bundle (mizumind/), and stage it into the public-web
# hosting downloads dir so the hosted zip can never drift from the bundle.
#
# The marketplace repo (this repo) is the single source of truth for plugin
# content (MIZUMIND-PLUGIN-ARCHITECTURE-v1). The hosted zip at
# https://mizumind.app/downloads/mizumind.plugin is a build artifact of it.
#
# Usage: scripts/build-plugin-zip.sh
# Then: commit the updated zip in public-web and deploy (approval-gated).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUNDLE_DIR="$REPO_ROOT/mizumind"
PUBLIC_WEB_DOWNLOADS="${PUBLIC_WEB_DOWNLOADS:-$HOME/prj/neuroarts-inc/public-web/hosting/public/downloads}"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

[ -f "$BUNDLE_DIR/.claude-plugin/plugin.json" ] || { echo "FATAL: $BUNDLE_DIR is not a plugin bundle (.claude-plugin/plugin.json missing)" >&2; exit 1; }

# Clean copy: no .DS_Store, no dotfile junk beyond the required .claude-plugin/.mcp.json
rsync -a --exclude '.DS_Store' "$BUNDLE_DIR/" "$STAGE/mizumind/"

OUT="$STAGE/mizumind.plugin"
(cd "$STAGE" && zip -q -r -X "$OUT" mizumind)

if [ -d "$PUBLIC_WEB_DOWNLOADS" ]; then
  cp "$OUT" "$PUBLIC_WEB_DOWNLOADS/mizumind.plugin"
  echo "OK: staged $(du -h "$PUBLIC_WEB_DOWNLOADS/mizumind.plugin" | cut -f1) -> $PUBLIC_WEB_DOWNLOADS/mizumind.plugin"
  echo "Next: commit in public-web + deploy (approval-gated)."
else
  cp "$OUT" "$REPO_ROOT/mizumind.plugin"
  echo "WARNING: public-web downloads dir not found at $PUBLIC_WEB_DOWNLOADS" >&2
  echo "Zip left at $REPO_ROOT/mizumind.plugin — move it manually." >&2
fi

unzip -l "${PUBLIC_WEB_DOWNLOADS}/mizumind.plugin" 2>/dev/null || unzip -l "$REPO_ROOT/mizumind.plugin"

# MizuMind plugin release checklist (ISS-232)

Source of truth for plugin content is this repo's `mizumind/` bundle
(MIZUMIND-PLUGIN-ARCHITECTURE-v1). Every plugin revision runs this list —
web assets update deliberately, never drift.

## 1. Bundle gates
- [ ] `claude plugin validate --strict mizumind/` passes clean.
- [ ] `mizumind/skills/mizu-help/references/verify-tool-catalog.sh` — generated
      catalog matches the connector's live `tools/list` (surface=v1) exactly.
- [ ] Skill descriptions lean; always-on token cost < ~300 (ISS-143).
- [ ] No CRM/StoryDrop/ops tools referenced anywhere in the public bundle.
- [ ] No internal codenames / tracker refs in any user-facing string (SO-014/SO-024).

## 2. Version
- [ ] While iterating: no `version` in plugin.json (commit SHA drives updates).
      Once pinned: bump semver deliberately — commits behind a pinned version ship nothing.

## 3. Marketplace lane (Claude Code — the update channel)
- [ ] Commit + push to `neuroarts/claude-plugins` (public).
- [ ] Fresh `/plugin marketplace add neuroarts/claude-plugins` + `/plugin install mizumind@neuroarts` works.

## 4. Web assets lane (Desktop / Cowork zip)
- [ ] Run `scripts/build-plugin-zip.sh` — rebuilds `mizumind.plugin` from the bundle
      and stages it into public-web `hosting/public/downloads/`.
- [ ] Commit the zip in public-web; setup page (`/mizumind/setup`) copy still accurate
      for all three lanes (web connector-only / desktop zip / code marketplace).
- [ ] Deploy public-web per SO-019 (explicit approval; batch at session close).

## 5. Fresh-profile verification (interactive — no false greens, ISS-144)
- [ ] Fresh profile: zip upload in Desktop/Cowork → OAuth completes → `whoami` returns.
- [ ] One natural-language trigger tested per skill (start/help/focus/journal/checkin).
- [ ] Anything unverifiable is flagged in the tracker, not marked done.

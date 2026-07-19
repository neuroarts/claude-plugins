---
description: First-run MizuMind orientation — confirm the connector is live and set the user's check-in mode once.
---

First-run orientation for the MizuMind wellness connector. Run this once when a user
installs the plugin:

1. Confirm the connector is authenticated by calling `whoami`. If it errors, tell the
   user the OAuth approval didn't complete and to re-enable the plugin — do not proceed.
2. Read `get_checkin_preference`. If `isDefault` is true, this is a first run — briefly
   explain the three check-in modes (Off / Standard 90-min / Gentle) and let the user
   pick one, then persist it with `set_checkin_preference`. If they don't choose, leave
   the default untouched.
3. Offer one time-appropriate practice now via `get_checkin_suggestion`, presented as a
   clean tap-to-open MizuMind link (never a raw URL, never a device timer).

Keep it to a few sentences — this is a warm hello, not a setup wizard. MizuMind is an
AI-assisted wellness connector by NeuroArts Interactive; practices open in the MizuMind
app and log to the user's real streak and history.

# MizuMind — Directory Submission Dossier

**Refreshed 2026-07-27.** Supersedes the 2026-07-18 dossier that lived in the archived
`mizumind-plugin` repo. Verified against Anthropic's live docs the same day
(`/docs/connectors/building/submission` and `/docs/connectors/building/review-criteria`).

---

## 0. Which repo, settled

**Canonical: `github.com/neuroarts/claude-plugins`** (public).

`neuroarts/mizumind-plugin` is an **empty repository** — 0 KB, "Git Repository is empty",
created 2026-07-18 and never pushed to. Its archived working copy on disk is named
`mizumind-plugin-DUPLICATE-superseded-by-claude-plugins`. Do not submit from it.

Multi-surface reuse (VS Code Copilot, and any future ChatGPT adapter) comes from the **MCP
server**, not from a plugin repo: ISS-166 verified that `mcp.neuroarts.ai/mcp` already serves
every standard MCP client through the same OAuth flow with zero per-surface changes. A Claude
plugin repo (marketplace.json, hooks, skills, commands, subagents) is Claude-specific by
construction and is not consumable by those surfaces.

---

## 1. Two submissions, not one

| | Plugin Directory | Connectors Directory |
|---|---|---|
| Artifact | the repo `neuroarts/claude-plugins` | the server `https://mcp.neuroarts.ai/mcp` |
| Where | `clau.de/plugin-directory-submission` (form) | claude.ai admin settings → directory submissions |
| Needs | public repo + `claude plugin validate` | Team/Enterprise org + directory-management access |
| State | **ready** | **deployed + verified**; blocked only on carousel screenshots |

---

## 2. Pinned submission target

```
repo   github.com/neuroarts/claude-plugins
ref    v1.1.7
sha    (resolve from the tag: `git rev-list -n1 v1.1.7`)
slug   mizumind
```


**Updated 2026-07-27 evening (was v1.1.6).** v1.1.6 does NOT contain the tool-catalogue
fix. It shipped `mizumind/skills/mizu-help/references/tool-catalog.md` naming two tools a
consumer cannot call — `mizu_focus_cockpit` (gated to business scopes, ISS-554) and
`create_issue` (pulled from the public surface) — and never mentioning the practice area
at all. Its sibling `verify-tool-catalog.sh` reported OK throughout, because it compares
the catalogue against a hardcoded list inside itself (ISS-563).

The fix landed in 6c56303, AFTER the tag. Pinning a tag is the right discipline — the
whole point of the note below — but a tag only pins what existed when it was cut, and
nothing re-checks that the pinned ref still contains the latest fix. Caught by asking what
`git show v1.1.6:tool-catalog.md` actually contains, rather than trusting that "the plugin
is fixed" meant "the pinned ref is fixed".

`claude plugin validate` re-run at v1.1.7: **passed**.

The sha is deliberately NOT written out here. A commit that records its own sha is
impossible — writing the number changes HEAD, and I chased that around three commits
before noticing. The TAG is the pin; resolve the sha from it at submission time. That is
also what the plugin form wants: it pins ref + sha, and the ref is the stable half.

**Updated 2026-07-27 (was v1.1.3 / 6b9e369).** v1.1.3 predates two behavioural fixes,
both for defects observed live in cloud Cowork: ISS-548 (the mizu-focus skill instructed
Claude to coach breathing in the chat — "or we do it right here, no app needed", which
logs nothing) and ISS-543 part 2 (the hook asserted a day-part computed from the naive
clock, which is the container's UTC in cloud Cowork).

**Do not submit v1.1.0 / 315a7f8**, which the old dossier names. It is 10 commits behind and
predates ISS-478's fix for a duplicate `hooks` reference that **crashed plugin load and left
the MCP server unregistered**. Submitting it would ship a plugin that does not work.

`claude plugin validate` — **passed**, re-run at v1.1.7 (2026-07-27). Plugin hook tests 36/36.

---

## 3. Listing copy

### Server name (≤100)
```
MizuMind
```

### Tagline (≤55) — 42 chars
```
Breathing, focus, and journaling in Claude
```

### Description (≤2000) — 1,204 chars
```
MizuMind brings a real practice into Claude. Ask for a breathing session, a focus
reset before deep work, or a wind-down at the end of the day, and Claude hands you a
session that opens in the MizuMind app.

The sessions are real. Every practice link opens the MizuMind portal and logs to your
actual history, streak, and progress — Claude never runs a timer in the chat or invents
an exercise. What you do in Claude and what you do in the app are the same record.

Suggestions are matched to the time of day. A morning ask and a late-night ask return
different practices, computed in your own timezone rather than the server's. If you are
part-way through a guided flow, MizuMind offers to resume that first.

You also get a private journal. Add an entry from any conversation, read back recent
ones, and see how entries trend over time. Entries written in the MizuMind app are
encrypted on your device and stay that way — this connector cannot read them and does
not try.

Connect with your MizuMind account. MizuMind acts only on your behalf, only for the
requests you make, and you can disconnect at any time.

MizuMind is a wellness practice, not medical care, therapy, diagnosis, or crisis
support.
```

_Counts verified programmatically 2026-07-27. Both had drifted — the tagline read 43 and
the description 1,143, because the copy was edited after the counts were written. Neither
was ever near its limit, so nothing was at risk; but a character count exists to prove the
field fits, and a count nobody re-runs is decoration. Re-measure after any copy edit._

### Categories (1–5, in order of fit)
```
productivity
```
`wellness` is **not** in the accepted enum on the plugin form
(development / productivity / database / monitoring / security / deployment / design /
learning / location / migration / math / testing / automation). Select `wellness` only if
the connector portal offers it. Keep wellness/mindfulness/breathing as keywords.

### Use cases (portal asks for primary use cases)
```
1. Take a guided breathing or focus session without leaving the conversation — the
   session opens in MizuMind and counts toward your real streak.
2. Get a practice matched to the current time of day and to whatever you are already
   part-way through.
3. Keep a private journal from inside Claude: add an entry, read recent ones, and see
   how they trend.
4. Browse the MizuMind catalog of breathing, focus, and wind-down exercises and open
   any of them directly.
```

### What users need before connecting
```
A MizuMind account — free, and created for you the first time you sign in with Google.
When you connect, MizuMind's OAuth page opens and you choose "Continue with Google";
if you have not used MizuMind before, that first sign-in creates your account. Existing
members can sign in with email and password instead. No plan or payment is required to
use the connector.
```

_Corrected 2026-07-27. The previous wording — "free to create at mizumind.app" — pointed
at a page with no signup: `/signup`, `/register` and `/login` all 404 on both
mizumind.app and flow.mizumind.app, and the OAuth page carries no sign-up link. Resolved
by reading the gateway rather than by testing in production: `src/lib/login-page.ts` uses
`signInWithPopup(auth, new GoogleAuthProvider())`, which auto-provisions in Firebase Auth
on first sign-in, while the email path is `signInWithEmailAndPassword` only — there is no
`createUserWithEmailAndPassword` anywhere in the gateway. So Google IS the account-creation
route and email/password is sign-in only. A reviewer without a Google account has no
self-serve path; that is a real constraint, now stated accurately instead of pointing at
a page where signup does not exist._

### Reads / writes
```
Both, scoped to your own MizuMind account.

Reads: your identity, profile, practice progress (streak, program day, in-progress
flows, recent sessions, active goal), check-in state and cadence, the breathing and
focus catalog, the guided video lessons, and your journal entries.

Writes: journal entries you ask it to add, practice sessions you ask it to log, your
practice goal, your check-in mode and interval, your profile preferences, feature
requests you choose to file, and the timestamp of your last check-in (delivering or
dismissing a check-in advances your cadence clock).
```

_Corrected 2026-07-27. The earlier text omitted three things the connector genuinely
does: it reads the **video lesson** catalog (`list_videos`, `recommend_video`), it writes
**feature requests** (`create_feature_request` files to the product backlog), and it
writes **your last-check-in timestamp** — `dismiss_checkin` always did, and ISS-574
established that `get_checkin_suggestion` and `checkin_status` do too, via `markCheckedIn`.
That last one was not knowable when the declaration was written, because those two tools
were annotated `readOnlyHint: true` at the time. Undeclared reads are untidy; undeclared
writes are the kind a reviewer is right to care about. Re-derive this field from
`tools/list` after any tool change._

### URLs
```
documentation   https://mizumind.app/mizumind/setup
privacy policy  https://mizumind.app/privacy
support         support@neuroarts.ai
homepage        https://mizumind.app
MCP endpoint    https://mcp.neuroarts.ai/mcp   (streamable HTTP, POST)
```

### Company
```
NeuroArts Interactive
https://mizumind.app
```

### Marketing constraint
Never claim "Anthropic Verified", "approved by Anthropic", or similar until it is literally
true. "Works with Claude" is fine. The two-tier model lists compliant servers as *Community*
automatically; verified escalation is Anthropic's call and is not requested.

---

## 4. Readiness ledger — verified, not assumed

| Requirement | State |
|---|---|
| OAuth 2.1 + PKCE (S256), no client_credentials | PASS — re-verified live 2026-07-26 |
| Protected Resource Metadata endpoint | PASS — 200, valid |
| 401 discovery contract + WWW-Authenticate | PASS — the #1 rejection cause, verified |
| Streamable HTTP over HTTPS, POST /mcp | PASS |
| Reachable from Anthropic cloud egress | PASS — this connector works in claude.ai today |
| Tool annotations (`title` + read/destructive hint) | PASS — 30/30, every tool on every surface |
| Tool names ≤ 64 chars | PASS |
| Privacy policy live, covers the connector | PASS — **content read and verified** 2026-07-27, see §5f |
| Public documentation URL | PASS — live, 3 steps + 4 sample prompts |
| Support contact | PASS |
| Reviewer test account | **REQUIRED** (docs: "have your ... test account credentials ready"; Test & launch step wants "credentials for a fully populated account"). PASS — exists, `products: []` verified with a control (§5h), timezone + history seeded 2026-07-28 |
| `claude plugin validate` | PASS — re-run at v1.1.7, 2026-07-27 |
| Origin-header validation | PASS — LIVE as of 4dcaab7f; authenticated calls unaffected |
| OAuth flow end-to-end (DCR -> authorize -> login) | PASS — probed live 2026-07-27, see §5d |
| PKCE **enforced**, not merely advertised | PASS — no-challenge and `plain` both rejected, see §5d |
| MCP Inspector run against the server | PARTIAL — every step verified live except the final code->token exchange, which needs an interactive login (§5d) |
| MCP Apps carousel screenshots | **REQUIRED — blocker.** Docs: MCP Apps "have the additional requirement of including screenshots". PNG, >=1000px, 3-5, cropped to the app response, no prompt in-image, prompts supplied separately, no video/GIF |
| Allowed link URIs declared | **NOT DONE** — must list `https://flow.mizumind.app` or users get an "Open external link" prompt on EVERY practice tap (§5i) |
| Separate read and write tools | PASS — the catch-all is no longer reviewer-visible (§5a) |
| Descriptions describe, do not instruct | PASS as of 5af49a69 — **was failing on 10 of 20**, see §5c |
| Consumer surface contains no v2/StoryDrop tools | PASS — exact-set pinned, see §5c |
| Card tap targets ≥ 44px | PASS as of a866eec9 — two of three were 16px/28px, see §5c |
| Time-of-day answers use the member's zone | PASS as of 39df3aad — **was failing in 2 of 3 paths**, see §5c |
| Every write tool has a reachable read surface | PASS — all 7 round-tripped live, see §5c |
| Crisis / self-harm guidance reaches every client | PASS as of d432b27f — **was plugin-only**, see §5e |
| readOnlyHint matches actual behaviour | PASS as of 6534888e — **2 tools wrote while claiming read-only**, see §5e |
| No business surface in ANY listing | PASS as of 8c3c6b7c — tools + resources + prompts + instructions, see §5e |
| Tool-routing eval after the description rewrite | **NOT RUN** — needs ANTHROPIC_API_KEY, see §5e |

---

## 5. The two things that could have got us rejected

### 5a. `mizu` is a catch-all command tool — FIXED 2026-07-27

Review criteria, verbatim:

> A single tool that accepts both safe HTTP methods (GET, HEAD, OPTIONS) and unsafe methods
> (POST, PUT, PATCH, DELETE) is rejected. Do not ship a catch-all `api_request` tool with a
> `method` parameter. … Documenting safe versus unsafe operations within one tool's
> description does not satisfy this requirement — the operations must be in separate tools.

`mizu` takes one freeform `command: string` and dispatches reads *and* writes across issues,
flows, crew, roles, community, and open. Its own source comment says "The mizu surface both
READS and WRITES" and sets `readOnlyHint: false, destructiveHint: false` — which is precisely
the "documented within one description" pattern the criterion rejects. It is present on
**both** the v1 and full surfaces.

**FIXED** (neuroarts-tech 1b0ff976, 4800d09a). `mizu` now requires a business grant
(ops or storydrop), so it is absent from a reviewer's tools/list.

The first attempt gated it on `MIZU_SURFACE=v1` and did nothing, because **production
does not set that flag** — see §8. The working fix gates on the token's product claim,
which holds regardless of surface.

Three more tools were pulled from the reviewer's view in the same pass:
- `create_issue` — a wellness listing should not offer "File an ops-backlog issue", and
  a reviewer's functional test would have written a real row into the live tracker.
  `create_feature_request` KEEPS its carve-out; that one is genuine member feedback.
- `update_issue` / `omoikane_write` — already claim-gated, confirmed hidden.
- `deploy` — was in tools/list for **every** signed-in identity, titled "Deploy a prod
  box service". Execution was always allowlisted and denied pre-action, so nothing was
  exploitable, but a public catalogue must not advertise infrastructure control. Now
  visible only to uids on `DEPLOY_OPERATOR_UIDS`, fail-closed when unset.

### 5b. Prescriptive tool descriptions — MEDIUM RISK

> Tool descriptions are rejected if they … Tell Claude to behave in ways unrelated to the
> tool's function … Describe what the tool does. Do not tell Claude how to behave.

Several of our descriptions carry presentation rules ("output structuredContent.display
VERBATIM", "NEVER print a bare/raw URL; a raw link is a hard fail") and cross-tool steering
("don't render the practice card for a focus result"). Those exist for good product reasons
(ISS-481/ISS-498) but read as behavioural instruction rather than description, and one of
them talks about *another tool*, which brushes against "interfere with Claude calling other
tools".

**Recommendation: keep the factual half, move the imperative half into the skills.** e.g.
"Returns a pre-rendered markdown summary in `structuredContent.display`" describes the tool;
"NEVER print a raw URL" instructs the model. The plugin's skills are the right home for the
second kind.

---

## 5c. Found after the v1 refocus — 2026-07-27

Bootstrap: *"stay focused on the v1 consumer edition, not the v2 internals — nothing in
v1 should involve storydrop."* Auditing against that sentence rather than against the
code found four things the earlier passes had not.

### The Today cockpit was in the consumer catalogue and had no wellness in it (ISS-554)

`mizu_focus_cockpit` registered unconditionally. Its only two sections are a StoryDrop
cohort pulse (`list_cohorts`) and an open ops-issue count (`list_issues`) — no wellness
content at all — and both feeding tools are gated, so for a reviewer every section
rendered an error card. Under `MIZU_SURFACE=v1` the business tools are not registered at
all, so on the exact surface a reviewer connects to it could only ever have shown two
errors. `iss-114-v1-surface.test.ts` had it pinned as a correct member of that surface.

Its description also read: *"surfaces a StoryDrop cohort pulse and the open ops-issue
count"* — in the catalogue a reviewer opens first.

Now gated on `ops || storydrop`. Consumer surface 21 → 20 tools.

### 10 of 20 descriptions told Claude how to behave (ISS-556)

Against the criterion *"Describe what the tool does. Do not tell Claude how to behave."*
The recurring shape was *"Do NOT invent an exercise yourself: always call this tool
so..."*; the live build still says *"output structuredContent.display VERBATIM ... Raw
links are a fail."*

Safe to remove because it was misplaced, not wrong: all of it already lives in
`SERVER_INSTRUCTIONS` and again in the mizu-focus skill. A third copy, in the one place
the criteria reject it. Rewrote 8; deliberately left `get_practice_progress` and
`dismiss_checkin`, which describe the tool rather than the model.

### The practice card's tap targets missed the mobile floor (ISS-555)

Now the only reviewer-visible card. `.resume` was ~16px and the alternate pills ~28px
against a 44px iOS/Material floor; `.start` passed only because 13px padding and a 15px
font happened to sum to 44. All three pinned explicitly, guarded against the *generated*
bundle rather than the shell it is built from.

### The consumer surface is now pinned as an EXACT set (ISS-552)

`iss-119` asserts the business tools are absent, from a hand-maintained list — which
cannot fail for a tool nobody added to it. Demonstrated: registering an ungated
`list_storydrop_partners` fails the new test twice while `iss-119` passes all four.
`tools/list` for a zero-product identity must now EQUAL the 20 named tools.

### What these four have in common

Every one was guarded by something that read a *copy* or a *list*, not the thing itself
— a test naming what must be absent, a description nobody asserted on, a CSS shell
rather than the shipped bundle. Same shape as ISS-545 earlier in the day, where four
green guards all read git while production sat eleven commits stale.

### The clock was the member's in only one of three places (ISS-561, ISS-562)

`suggest_focus_exercise`, probed live at 16:53 America/Chicago, answered a **deep-work**
request with *"Midnight Breathing — Moon & stars sleep wind-down."* Minutes earlier
`get_checkin_suggestion` had correctly said dayPart "noon" for the same account. Two
tools disagreed about what time it was for the same member in the same minute.

Both focus lookups derived the hour from `now.getHours()` — the server clock, UTC on the
box. ISS-500 fixed exactly this for check-ins by threading `users/{uid}.timezone` through
`hourInZone`; the focus path shares the same ladder and never got it.

Sweeping the class found a third: `distinctDays` in journal-trends carried the docstring
"Distinct **local** calendar days" over a body using `toISOString()` — UTC. For an app
about evenings that is wrong in both directions, and it is shown to the member as
"N entries across N days in the last 7 days".

All three now resolve in the member's zone and report which clock they used.

### Every write tool round-tripped (ISS-558, ISS-559, ISS-560)

Checked each of the seven v1 write tools for a **reachable** read surface. Two failed:
`update_user_preference` wrote a document nothing governing check-ins reads (proven live
— the settings echo back saved and `nextCheckinAt` does not move), and
`set_practice_goal` was orphaned when we removed the `mizu` catch-all earlier the same
day, leaving no v1 tool able to read a goal back. Round-tripping the journal then
surfaced ciphertext reaching members on structuredContent-rendering hosts.

### What these have in common with §5c above

Every one was guarded by something that read a copy, a list, or the easy half: a test
naming what must be absent, a description nobody asserted on, a CSS shell rather than the
shipped bundle, a doubles-set that implemented only the write. Twice the full suite passed
**identically** before and after a real fix, which is the cheapest signal that nothing was
pinning the thing at all.

---

## 5d. OAuth gate — probed live against production, 2026-07-27

The #1 documented rejection cause, verified by exercising it rather than by reading the
metadata. Everything below is against `auth.neuroarts.ai` / `mcp.neuroarts.ai` after the
`4c8b6d69` deploy.

| Step a reviewer's client takes | Probe | Result |
|---|---|---|
| Discover the resource | unauthenticated POST /mcp | 401 + `WWW-Authenticate` naming the PRM |
| Read Protected Resource Metadata | GET /.well-known/oauth-protected-resource | 200, `resource` exactly matches the endpoint |
| Read AS metadata | GET /.well-known/oauth-authorization-server | S256 only, no client_credentials, DCR present |
| **Register a new client (DCR)** | POST /register | **201**, public client (`token_endpoint_auth_method: none`), `offline_access` granted |
| Start the flow with PKCE | GET /authorize + S256 challenge | 200, "Sign in to MizuMind" |
| Final code -> token exchange | — | NOT probed: needs an interactive login |

### PKCE is ENFORCED, not just advertised

The distinction matters: metadata can claim S256 while the endpoint accepts anything.
Both negative cases were probed.

    no code_challenge   -> 302 to the client's redirect_uri with
                           error=invalid_request
                           error_description="code_challenge required (PKCE S256)"
    method=plain        -> 302 ... "Only code_challenge_method=S256 is supported"
    client_credentials  -> {"error":"unsupported_grant_type"}

Both rejections are spec-correct error redirects rather than bare 400s, and both carry
the `iss` parameter (RFC 9207 issuer identification — the authorization-server mix-up
defence). That is a detail most implementations omit.

The only untested link in the chain is the final code->token exchange, which cannot be
driven without an interactive sign-in. Cowork performs exactly that step when it signs
in as the reviewer account, so the chain closes there.

---

## 5e. Post-deploy sweep — 2026-07-27 evening

Everything below was found AFTER the 22:23Z deploy of `4c8b6d69`, so it is fixed in git
and **not yet in production** unless a later deploy has run. Check
`ops/scripts/check_deployed_connector_current.py` before assuming.

### Crisis guidance reached only plugin users (ISS-572)

`SERVER_INSTRUCTIONS` — the text every client receives on `initialize` — contained **zero**
crisis, self-harm, medical, therapy or scope language. The only such guidance lived in
`mizu-focus/SKILL.md`, which ships in the **plugin**. A client that connects the MCP
server without installing the plugin — exactly what a directory reviewer does — got a
connector that proactively offers wellness practices and says nothing about any of it.

The eval already encoded the requirement: its hardest negative case is *"I've been having
thoughts of hurting myself"*, expect `no_call`. Nothing in the shipped instructions
enforced it. Added, with a pointer to 988 / local emergency services.

### Two tools claimed readOnlyHint while writing (ISS-574)

`get_checkin_suggestion` and `checkin_status` both call `markCheckedIn()`, persisting
`lastCheckinAt`. Both were annotated `readOnlyHint: true`. Hosts use that hint to decide
what runs WITHOUT asking, so a host auto-approving read-only tools was silently
rescheduling members' check-ins.

Found only after distrusting an earlier check of mine that verified annotations against a
write-set assembled from tool NAMES. The replacement derives the answer from the handler
(recording proxy over each store) and checks BOTH directions — the reverse assertion is
what caught `checkin_status`.

### The business surface leaked from four places, one at a time (ISS-554/566/567/569/570)

`tools/list` -> `resources/list` -> `prompts/list` -> `initialize` -> a tool description.
Each was found only after fixing the one before it. `prompts/list` carried *"Query the
StoryDrop CRM"*; `/help` described the ops backlog and named a dozen tools a consumer
cannot call, with wellness mentioned once. The fix that matters is the last one: a single
guard that sweeps EVERY consumer-visible string in one pass, rather than one surface at a
time.

### Known-unmeasured: tool routing (ISS-571)

ISS-556 removed behavioural instruction from nine descriptions, correctly — and removed
the situational vocabulary with it ("help me focus", "I need a break"), which is
precisely what the ISS-408 eval uses as its golden cases. Restored as coverage rather
than command, but **routing quality after both edits has never been measured**. The
instrument is `eval/run-live.ts` (60 cases, thresholds 0.90 should-call / 0.95
should-not-call); it needs `ANTHROPIC_API_KEY`. Run it before submitting if a key is
available. Not a blocker — the descriptions are conservative and every tool was exercised
by hand — but it is a known-unmeasured risk rather than a known-good state.

---

## 5f. Privacy policy — read, not just reachable (2026-07-27)

Previously the ledger recorded this as PASS on the basis of a 200 and a section number.
Fetched and read the actual text. Section 7, "MizuMind in Claude (Connector and Plugin)",
covers everything a reviewer looks for:

  - the endpoint by name (mcp.neuroarts.ai) and the plugin
  - OAuth with the exact scopes requested — openid, profile, email, offline_access,
    which matches what auth.neuroarts.ai's metadata actually advertises (§5d)
  - what the connector does on the member's behalf, scoped to their own account
  - journal note content encrypted at rest, stored as ciphertext
  - local plugin data: tool names and timestamps only, never arguments, responses or
    journal content; never leaves the device
  - what is shared with Anthropic, and only to fulfil requests made in a session
  - "Removing or disabling the connector or plugin ends its access at any time"
  - elsewhere: "We DO NOT sell your personal data", and account deletion

### The AI disclosure was already right — the connector was not

Section 7 carries an explicit AI disclosure: *"MizuMind in Claude is an AI-assisted
wellness companion... It is not medical care, therapy, diagnosis, or crisis counseling."*

That promise has been public for some time. Until ISS-572 this evening, SERVER_INSTRUCTIONS
contained no crisis, self-harm or scope language at all — so the policy told members what
the connector would not do, and nothing in the connector enforced it. The two now agree.

Worth noting for its own sake: a published promise is not an implemented one, and the gap
between them is invisible from either side alone.

---

## 5g. Every claim in the listing copy, checked against the running connector

The description is not marketing that sits beside the product — each sentence is a
promise a reviewer can test in one call. Verified 2026-07-27 against the deployed build.

| claim in the submitted copy | verified how | state |
|---|---|---|
| "a session that opens in the MizuMind app" | every portalUrl is flow.mizumind.app | LIVE |
| "logs to your actual history, streak, and progress" | log_practice_session -> get_practice_progress round trip | LIVE |
| "Claude never runs a timer in the chat or invents an exercise" | SERVER_INSTRUCTIONS "NEVER substitute a device timer" | LIVE |
| "Suggestions are matched to the time of day" | get_checkin_suggestion returned dayPart "evening" at 18:5x local | LIVE |
| **"computed in your own timezone rather than the server's"** | `resolvedFromMemberZone: true` — 23:5x UTC would be *bedtime*, it correctly returned evening | **LIVE, but only since ISS-561 today** |
| "offers to resume that first" | the resume line is the FIRST element of `display` | LIVE |
| "see how entries trend over time" | list_journal_entries returns a `trends` block | LIVE |
| "encrypted on your device ... this connector cannot read them and does not try" | ciphertext preserved in `notes`, rendered as an explanation (ISS-560) | LIVE |
| "you can disconnect at any time" | OAuth; privacy policy §7 states it | LIVE |
| **"not medical care, therapy, diagnosis, or crisis support"** | the copy is accurate as a disclaimer, but until ISS-572 nothing in the connector ACTED on it | **STAGED, NOT DEPLOYED** |

### What this exercise was actually for

Two of the claims we are submitting were **not true of the connector** when they were
written:

  - the timezone sentence was false for `suggest_focus_exercise` until ISS-561 this
    afternoon — it answered a 16:53 deep-work request with "Midnight Breathing" off the
    server clock
  - the crisis disclaimer was accurate as a statement about the product, while the
    connector itself carried no crisis, self-harm or scope guidance for any client that
    had not installed the plugin (ISS-572, still undeployed)

Nobody wrote either claim dishonestly. They describe what the product is meant to be, and
the drift between intent and implementation is invisible unless someone reads the copy
with the running system in front of them. That is the whole exercise: marketing copy is a
specification nobody tests.

---

## 5h. What the reviewer sees — now MEASURED, not inferred (2026-07-27 19:3x)

§5b/§5c established the consumer surface as a chain of four facts, one of which was an
assumption: *"a reviewer holds no products."* That link is now measured against the real
account, using the production entitlement store reading production Firestore:

    mizumind-reviewer@neuroarts.ai   products = []
    reviewer@neuroarts.ai            products = []
    bootstrap (control)              products = ["storydrop","ops"]

The control matters. Without it, `[]` is equally consistent with a store that is broken
and returns nothing for everyone — which would have looked like a pass while proving the
opposite. Bootstrap's account returning its two real grants shows the store is genuinely
reading Firestore.

So the full chain, every link now verified rather than assumed:

1. deployed source == origin/main — `check_deployed_connector_current.py`, all 72 files,
   process started after the newest file
2. origin/main vends EXACTLY 20 tools to an identity with `products: []` —
   `iss-552-v1-consumer-surface-exact.test.ts`, mutation-verified
3. the entitlement gate is ENABLED in production — `ENTITLEMENTS_DISABLED` absent from
   run-mcp.sh, the systemd unit and `/proc/<pid>/environ`; the running process logged
   "entitlements: ENABLED"
4. **the reviewer account genuinely has `products: []`** — measured above, with a control

A reviewer signing in to either account gets the 20-tool wellness surface. The only thing
still unverified is the final OAuth code->token exchange, which needs an interactive
sign-in and is the first thing Cowork does.

### Two data gaps on the account that affect the CAPTURES, not the surface

`timezone: null` and zero practice history on both accounts. Neither changes what tools
are vended; both change what the screenshots show — an untimezoned account computes the
day-part from the box's UTC clock, and an empty account renders "No practice history
yet". Detail and fix in the reviewer-account handoff.

---

## 5i. Requirements re-verified against the live docs — 2026-07-28

Two rows in this ledger had no citation, and on 2026-07-28 I told Bootstrap the test
account was probably not required because I could not find the requirement. That was
wrong: "I could not find it" is not "it is not required". Both are documented at
`claude.com/docs/connectors/building/submission`.

**Screenshots — required, because MizuMind is an MCP App:**
> "MCP Apps — MCP servers that surface interactive UI elements. These have the
> additional requirement of including screenshots for submission and listing."

Spec: PNG, width >= 1000px, count 3-5, cropped to the app response with the prompt NOT
in the image, any aspect ratio, prompt text supplied separately per screenshot, no
separate mobile assets, video/GIF not accepted. A carousel template exists in the
Anthropic MCP Apps Figma community file.

**Test account — required:**
> "Before you start, have your documentation URL, privacy policy URL, icon, and test
> account credentials ready"

and the portal's Test & launch step wants "access instructions detailed enough for a
reviewer to access your server end to end: every link, credential, and step, including
credentials for a fully populated account where relevant." That clause is why the
reviewer account was seeded with practice history and journal entries.

### NEW, and not previously tracked: allowed link URIs

> "If your connector uses the `ui/open-link` capability to open URLs ... provide the list
> of link targets your server will request. Claude uses this list to suppress the 'Open
> external link' confirmation prompt for destinations you've declared."

Every practice this connector surfaces is a `flow.mizumind.app` deep-link, so without
this every single tap costs the member a confirmation dialog. Declare
`https://flow.mizumind.app`. Origins must be owned by the submitting organization —
this one is. Optional field, but omitting it degrades the core interaction.

### Other portal facts worth having before starting

  - the portal saves progress per browser session; you can move between steps
  - Compliance is SEVEN required acknowledgments (directory guidelines, first-party API
    use, financial transactions, AI media generation, prompt injection, conversation data
    collection, public documentation)
  - Test & launch also asks you to CONFIRM you have run every tool yourself, via MCP
    Inspector or as a custom connector. Our ledger's Inspector row is that confirmation.
  - listing limits confirmed: name <= 100, tagline <= 55, description <= 2000, 1-5
    categories, plus a permanent URL slug

---

## 6. What only a human can do

1. **Capture 3–5 carousel screenshots** — see §10. The naive "one per card" plan is WRONG
   and would have leaked customer data.
2. **Confirm the org is Team or Enterprise** with directory-management access.
3. **Submit the forms** and complete the live OAuth click-through.
4. **Deploy the connector** so the Origin-validation hardening is live before a reviewer probes it.

---

## 7. Tool count — what a reviewer actually sees

Best practice we researched previously: roughly 15-20 tools, ~4 sentences each.

**A zero-grant reviewer now sees 20 tools, all wellness:**

```
checkin_status, create_feature_request, create_journal_entry, dismiss_checkin,
get_checkin_preference, get_checkin_suggestion, get_journal_entry,
get_practice_progress, get_user_profile, list_journal_entries, list_videos,
list_wellness_tools, log_practice_session, mizu_practice_card,
recommend_video, set_checkin_preference, set_practice_goal, suggest_focus_exercise,
update_user_preference, whoami
```

An allowlisted operator with ops+storydrop still sees all 30 — nothing was removed from
the product, only from the public catalogue.

20 lands exactly on the researched target. It was 21 until `mizu_focus_cockpit` was
gated out as business-scoped (ISS-554, see §10) — that removal was made because the
cockpit renders only StoryDrop and ops data, not to hit a number. Tool COUNT is not a
documented rejection cause in any case; tool DESIGN is.

## 8. The endpoint is not what the repo said it was

Worth its own section, because it invalidated an earlier fix and a prior dossier.

`mcp.neuroarts.ai/mcp` does **not** serve a wellness-only surface. Verified on the box:
`/opt/connector/run-mcp.sh` carries `# MIZU_SURFACE removed 2026-07-09 (Bootstrap: SINGLE
user-gated endpoint on the clean URL; v1 split retired)`, and Caddy maps
`mcp.neuroarts.ai -> 127.0.0.1:4100 -> that script`. Unset ⇒ the FULL surface.

The repo's `deploy/run-mcp.sh` still exported `MIZU_SURFACE=v1` and the deploy README's
topology table still called port 4100 "V1 wellness-only". Both are corrected as of
2026-07-27. Naming trap worth remembering: the host *called* `mcp-v1...` is the BUSINESS
surface, not v1.

Practical consequence: **all gating that matters is per-identity**, not per-endpoint. That
is why the fixes in §5a are written against product claims and the deploy allowlist.


---

## 9. Deploy verification — 2026-07-27

**Deployed build `4dcaab7f` at 19:35:40Z.** Production had been eleven connector commits
behind (`2b9a3495`, 2026-07-25); every fix in §5 now exists where a reviewer will look.

| check | result |
|---|---|
| `check_deployed_connector_current.py` | **OK — all 72 deployed files match `origin/main`** |
| restart followed the sync | process 19:35:43Z, newest file 19:35:40Z |
| `whoami` build stamp | **`4dcaab7f`**, deployedAt `2026-07-27T19:35:40Z` (was `"dev"`) |
| tool title drift (ISS-545 symptom) | **"Morning Practice"** — the rename is live |
| `resolvedFromMemberZone` | **`true`** (ISS-535 #2 and #3, closed) |
| `dayPart` at 14:36 CDT | **`noon`** — canonical 5/12/17/21 ladder |
| `display` field, resume link | present; the resume store-check ran and kept a valid link |

### Protocol bar, re-verified against the deployed build

```
POST /mcp (unauth, initialize)
  HTTP/2 401
  www-authenticate: Bearer resource_metadata="https://mcp.neuroarts.ai/.well-known/
                    oauth-protected-resource", error="invalid_token",
                    error_description="missing Authorization header"
```

That is the #1 documented rejection cause and it is correct. PRM returns 200 with
`resource`, `authorization_servers: [auth.neuroarts.ai]`, `scopes_supported`,
`bearer_methods_supported`.

**Origin validation is live and did not break the endpoint.** Unauthenticated probes with
`Origin: https://claude.ai`, `Origin: https://evil.example`, and no Origin all return 401 —
inconclusive by design, because auth runs before the transport. The decisive evidence is
that AUTHENTICATED calls (`whoami`, `list_wellness_tools`, `get_checkin_suggestion`) all
succeeded immediately after the deploy, which is the safety property that mattered: a
request with no Origin header is the server-to-server path Anthropic's cloud egress uses.

### MCP Inspector — partial, and honestly so

`npx @modelcontextprotocol/inspector --cli https://mcp.neuroarts.ai/mcp --method tools/list`
connects and receives the correct 401 JSON-RPC error. That verifies reachability and the
discovery contract through Anthropic's own tool.

Exercising every tool through the Inspector requires a bearer token from the interactive
OAuth flow, which is a human step. The submission portal asks you to confirm you have run
every tool "via MCP Inspector **or** as a custom connector in Claude" — the second path is
satisfied: the read-only surface was exercised live this session and every tool returned
real structured data, no generic errors. The write tools were deliberately not fired
against a real member account; that is what the reviewer test tenant is for.

### Not verifiable from here

The **20-tool zero-grant view** is unit-tested and mutation-verified, but cannot be
confirmed live from this session: the signed-in identity carries `ops` and `storydrop`
grants and therefore sees all 30. Confirming it live needs the reviewer test account —
worth doing before submitting, since it is the exact view a reviewer gets.


---

## 10. Carousel capture — corrected 2026-07-27 after a live run

An earlier draft of this dossier said "one per card is the natural set: practice card,
Today cockpit, CRM card." **Do not do that.** A Cowork run against the deployed build
found two reasons, one of them serious.

### The CRM card must not be in the carousel

`mizu_crm_card` **is not in the reviewer's 20-tool view.** Verified: it requires a
StoryDrop grant plus StoryDrop backend config, so a no-grant reviewer never sees the tool
at all. A carousel image of a card a reviewer cannot reach invites the obvious question,
and the listing would be advertising a surface the listing does not grant.

Worse, the live capture **showed real lead names and real account names**. That image
cannot ship publicly under any circumstance — it is customer data, and a directory
carousel is a public asset. Discard any CRM capture already taken; do not crop around it.

### Shoot from the REVIEWER TENANT, not an operator account

Sign in as `mizumind-reviewer@neuroarts.ai` (no grants) and capture from there, so the
images match exactly what a reviewer gets. A shot taken from Bootstrap's identity shows
content a reviewer never sees — a carousel that misrepresents the product to the person
checking whether the carousel represents the product.

### The Today cockpit is OUT — of the carousel and of v1 (ISS-554, 2026-07-27)

An earlier version of this section planned image 3 as "Today cockpit — wellness-only
state, as a reviewer sees it." **There is no such state.** The cockpit has exactly two
data sections, a StoryDrop cohort pulse (`list_cohorts`) and an open ops-issue count
(`list_issues`), and no wellness content whatsoever. For a no-grant reviewer both of
those tools are gated, so every section renders an error card.

Under `MIZU_SURFACE=v1` it was worse: the business tools are not registered at all, so
the cockpit could only ever have rendered two errors on the very surface a reviewer
connects to — and `iss-114-v1-surface.test.ts` pinned it as a correct member of that
surface, which is why nobody noticed.

Its description also read, to every reviewer opening tools/list: "surfaces a StoryDrop
cohort pulse and the open ops-issue count." A wellness connector advertising a CRM
pulse and an ops tracker invites precisely the question we do not want asked.

`mizu_focus_cockpit` is now gated on `ops || storydrop` alongside the tools it calls.
Operators keep it unchanged; the consumer catalogue drops from 21 tools to 20. Pinned by
`iss-552-v1-consumer-surface-exact.test.ts`.

### The set, given ONE reviewer-visible card

The only reviewer-visible ui:// resource is now `mizu_practice_card`. The spec wants 3–5
images and nothing requires each to be a different card, so lead with the card and fill
out with real tool responses:

1. Practice card — morning/daytime suggestion
2. Practice card — evening/wind-down suggestion (different day-part, different sessions)
3. `list_wellness_tools` catalogue response — a real app response, no card
4. *(optional)* `get_practice_progress` — streak + resume line, real data
5. *(optional)* a journal read-back

Same spec as before: PNG, ≥1000px wide, cropped to the app response with no prompt
visible, prompt text supplied separately, no video/GIF.

### Capture mechanics

The Chrome extension's own screenshots cap at CSS resolution (~734px, saved at 609px JPEG),
which fails both the format and the width requirement. The native screen buffer via the
device bridge yields higher-res PNG, but needs the card's tab frontmost. Plan for a
human-in-the-loop capture rather than an automated one.

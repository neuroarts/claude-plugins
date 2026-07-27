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
ref    v1.1.5
sha    (resolve from the tag: `git rev-list -n1 v1.1.5`)
slug   mizumind
```

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

`claude plugin validate` — **passed** at v1.1.4. Plugin hook tests 36/36.

---

## 3. Listing copy

### Server name (≤100)
```
MizuMind
```

### Tagline (≤55) — 43 chars
```
Breathing, focus, and journaling in Claude
```

### Description (≤2000) — 1,143 chars
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
A MizuMind account (free to create at mizumind.app). Sign in happens through MizuMind's
OAuth flow when you connect. No plan or payment is required to use the connector.
```

### Reads / writes
```
Both. Reads: your profile, practice progress, check-in state, the exercise catalog,
your journal entries. Writes: journal entries you ask it to add, logged practice
sessions, your check-in interval and practice goals.
```

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
| Privacy policy live, covers the connector | PASS — section 7, "Last Updated: July 2026" |
| Public documentation URL | PASS — live, 3 steps + 4 sample prompts |
| Support contact | PASS |
| Reviewer test account | reported done (mizumind-reviewer@) — **not re-verified by me** |
| `claude plugin validate` | PASS at v1.1.3 |
| Origin-header validation | PASS — LIVE as of 4dcaab7f; authenticated calls unaffected |
| MCP Inspector run against the server | PARTIAL — connects, 401 contract verified; tool exercise needs an interactive OAuth token (§9) |
| MCP Apps carousel screenshots | **MISSING — blocker** |
| Separate read and write tools | PASS — the catch-all is no longer reviewer-visible (§5a) |

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

## 6. What only a human can do

1. **Capture 3–5 carousel screenshots** — see §10. The naive "one per card" plan is WRONG
   and would have leaked customer data.
2. **Confirm the org is Team or Enterprise** with directory-management access.
3. **Submit the forms** and complete the live OAuth click-through.
4. **Deploy the connector** so the Origin-validation hardening is live before a reviewer probes it.

---

## 7. Tool count — what a reviewer actually sees

Best practice we researched previously: roughly 15-20 tools, ~4 sentences each.

**A zero-grant reviewer now sees 21 tools, all wellness:**

```
checkin_status, create_feature_request, create_journal_entry, dismiss_checkin,
get_checkin_preference, get_checkin_suggestion, get_journal_entry,
get_practice_progress, get_user_profile, list_journal_entries, list_videos,
list_wellness_tools, log_practice_session, mizu_focus_cockpit, mizu_practice_card,
recommend_video, set_checkin_preference, set_practice_goal, suggest_focus_exercise,
update_user_preference, whoami
```

An allowlisted operator with ops+storydrop still sees all 30 — nothing was removed from
the product, only from the public catalogue.

21 is one over the 20 target and that is fine: tool COUNT is not a documented rejection
cause, tool DESIGN is. If you want 20 exactly, fold the check-in preference pair
(`get_checkin_preference` / `set_checkin_preference`) into one.

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

The **21-tool zero-grant view** is unit-tested and mutation-verified, but cannot be
confirmed live from this session: the signed-in identity carries `ops` and `storydrop`
grants and therefore sees all 30. Confirming it live needs the reviewer test account —
worth doing before submitting, since it is the exact view a reviewer gets.


---

## 10. Carousel capture — corrected 2026-07-27 after a live run

An earlier draft of this dossier said "one per card is the natural set: practice card,
Today cockpit, CRM card." **Do not do that.** A Cowork run against the deployed build
found two reasons, one of them serious.

### The CRM card must not be in the carousel

`mizu_crm_card` **is not in the reviewer's 21-tool view.** Verified: it requires a
StoryDrop grant plus StoryDrop backend config, so a no-grant reviewer never sees the tool
at all. A carousel image of a card a reviewer cannot reach invites the obvious question,
and the listing would be advertising a surface the listing does not grant.

Worse, the live capture **showed real lead names and real account names**. That image
cannot ship publicly under any circumstance — it is customer data, and a directory
carousel is a public asset. Discard any CRM capture already taken; do not crop around it.

### Shoot from the REVIEWER TENANT, not an operator account

The Today cockpit renders **StoryDrop and ops-backlog business data when the caller holds
operator grants**. A cockpit shot taken from Bootstrap's identity therefore shows content a
reviewer will never see — a carousel that misrepresents the product to the person checking
whether the carousel represents the product.

So: sign in as `mizumind-reviewer@neuroarts.ai` (no grants) and capture from there. That
single change fixes both problems at once — no business data, no unreachable cards, and
the images match exactly what a reviewer gets.

### The set, given only two reviewer-visible cards

Reviewer-visible ui:// resources are `mizu_practice_card` and `mizu_focus_cockpit`. The
spec wants 3–5 images, and nothing requires each to be a different card:

1. Practice card — morning/daytime suggestion
2. Practice card — evening/wind-down suggestion (different day-part, different sessions)
3. Today cockpit — wellness-only state, as a reviewer sees it
4. *(optional)* `list_wellness_tools` catalogue response — a real app response, no card
5. *(optional)* a journal read-back

Same spec as before: PNG, ≥1000px wide, cropped to the app response with no prompt
visible, prompt text supplied separately, no video/GIF.

### Capture mechanics

The Chrome extension's own screenshots cap at CSS resolution (~734px, saved at 609px JPEG),
which fails both the format and the width requirement. The native screen buffer via the
device bridge yields higher-res PNG, but needs the card's tab frontmost. Plan for a
human-in-the-loop capture rather than an automated one.

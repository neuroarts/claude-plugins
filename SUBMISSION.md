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
| State | **ready** | blocked on carousel screenshots |

---

## 2. Pinned submission target

```
repo   github.com/neuroarts/claude-plugins
ref    v1.1.3
sha    6b9e369
slug   mizumind
```

**Do not submit v1.1.0 / 315a7f8**, which the old dossier names. It is 10 commits behind and
predates ISS-478's fix for a duplicate `hooks` reference that **crashed plugin load and left
the MCP server unregistered**. Submitting it would ship a plugin that does not work.

`claude plugin validate` — **passed** at v1.1.3.

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
| Tool annotations (`title` + read/destructive hint) | PASS — 23/23 on v1, 30/30 on full |
| Tool names ≤ 64 chars | PASS |
| Privacy policy live, covers the connector | PASS — section 7, "Last Updated: July 2026" |
| Public documentation URL | PASS — live, 3 steps + 4 sample prompts |
| Support contact | PASS |
| Reviewer test account | reported done (mizumind-reviewer@) — **not re-verified by me** |
| `claude plugin validate` | PASS at v1.1.3 |
| Origin-header validation | fixed in source, **NOT DEPLOYED** |
| MCP Inspector run against the server | **NOT DONE** |
| MCP Apps carousel screenshots | **MISSING — blocker** |
| Separate read and write tools | **AT RISK — see §5** |

---

## 5. The two things that can get us rejected

### 5a. `mizu` is a catch-all command tool — HIGH RISK

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

**Recommendation: drop `mizu` from the submitted surface.** Everything a member needs is
already covered by the purpose-built tools; `mizu` is an operator convenience. That also
takes v1 from 23 tools to 22.

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

1. **Capture 3–5 carousel screenshots** — PNG, ≥1000px wide, cropped to the app response
   only (no prompt visible), prompt text supplied separately, no video/GIF. One per card is
   the natural set: practice card, Today cockpit, CRM card. These must come from a live
   Claude session with real data — a headless render of the card HTML would be an empty
   shell, since the cards fetch through the MCP-Apps host bridge.
2. **Confirm the org is Team or Enterprise** with directory-management access.
3. **Submit the forms** and complete the live OAuth click-through.
4. **Deploy the connector** so the Origin-validation hardening is live before a reviewer probes it.

---

## 7. Tool-count note

Best practice we researched previously: roughly 15–20 tools, ~4 sentences of description each.

Actual today: **v1 = 23 tools, full = 30.** Dropping `mizu` (§5a) puts v1 at 22. Getting to
20 would mean folding two more — the check-in preference pair (`get_checkin_preference` /
`set_checkin_preference`) and the profile pair (`get_user_profile` /
`update_user_preference`) are the obvious candidates, but neither is required for review and
both are cheap to leave. Tool *count* is not itself a documented rejection cause; tool
*design* (§5a) is.

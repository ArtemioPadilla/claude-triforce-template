# Feature: Agent Triforce — Growth Plan
**Status**: Approved
**Priority**: P1-High
**Date**: 2026-02-26
**Tier**: M

---

## Problem Statement

Agent Triforce is a fully implemented, installable Claude Code plugin with a genuine methodological differentiator (Gawande/Boeing checklist framework applied to multi-agent AI development). It has been public for 12 days, has 1 GitHub star, 0 forks, and no organic discovery.

Three curated list submissions were attempted. One was closed (wrong submission method, wrong category framing). Two remain open and unreviewed. No content has been published. No community exists.

**For whom**: The maintainer — a solo developer who needs a realistic, sequenced plan to go from 1 star to meaningful adoption without wasted effort on channels that will not convert at this stage.

**The core problem is not the product. It is sequencing.** Promotion before proof fails. Curated list submissions before repo maturity get rejected. Content without social proof gets ignored. This plan sequences actions so each wave builds credibility for the next.

---

## Glossary

- **Repo age**: Days since the repository was created (currently: 12 days as of 2026-02-26)
- **Social proof threshold**: Minimum star count / fork count / commit history that makes a repo credible to gatekeepers and strangers
- **Methodology angle**: Leading with the Gawande/Boeing intellectual argument rather than "I built a plugin"
- **Orchestrator fatigue**: The documented tendency of awesome-claude-code maintainers to deprioritize multi-agent orchestration tools due to oversupply
- **PR #819**: The closed hesreallyhim/awesome-claude-code submission — wrong method (PR instead of issue), wrong framing (orchestrator)
- **ccplugins PR #46**: OPEN at `ccplugins/awesome-claude-code-plugins` — submitted correctly, no review yet
- **buildwithclaude PR #67**: OPEN at `davepoon/buildwithclaude` — submitted correctly, no review yet

---

## Success Metrics

### Phase 0 — Pre-Launch (Now through Week 2)
| KPI | Current | Target | Measurement |
|-----|---------|--------|-------------|
| Repo age | 12 days | 30 days | Calendar |
| GitHub stars | 1 | 10 | GitHub repo |
| README completeness | Unknown | Demo video linked, install verified, methodology section above fold | Manual checklist |
| Broken install path | Unknown | Zero broken steps verified on clean machine | Manual test |

### Phase 1 — Soft Launch (Weeks 3-6)
| KPI | Current | Target | Measurement |
|-----|---------|--------|-------------|
| GitHub stars | 1 | 50 | GitHub |
| Curated list acceptances | 0 | 2 | Manual tracking |
| Show HN points | N/A | 30+ | HN submission score |
| GitHub topics applied | 8 | 8 (verify all correct) | GitHub repo topics |

### Phase 2 — Content Momentum (Months 2-3)
| KPI | Target | Measurement |
|-----|--------|-------------|
| GitHub stars | 150 | GitHub |
| Reddit posts (combined upvotes) | 200+ | Reddit |
| Demo video views | 500+ | YouTube/Loom |
| hesreallyhim resubmission | Accepted or in-review | Issue tracker |

### Phase 3 — Community (Months 3-6)
| KPI | Target | Measurement |
|-----|--------|-------------|
| GitHub stars | 500 | GitHub |
| Product Hunt upvotes | 200+ | Product Hunt |
| GitHub Discussions threads | 10+ active | GitHub |
| First consulting inquiry | 1 | Inbound email/Discussions |

---

## User Stories

### Story 1: Pre-launch readiness
As the maintainer, I want to verify the repo is launch-ready before any promotion, so that a developer's first impression is polished and the install works without hand-holding.

**GIVEN** I have never seen the repo before,
**WHEN** I visit the GitHub page and follow the README,
**THEN** I can install the plugin, run `/feature-spec hello world`, and see the expected output — in under 10 minutes with no errors.

### Story 2: Curated list presence
As the maintainer, I want Agent Triforce accepted to at least 2 curated lists within 60 days, so that discovery happens through trusted community channels without paid promotion.

**GIVEN** ccplugins PR #46 and buildwithclaude PR #67 are already open,
**WHEN** I monitor their status and follow up appropriately,
**THEN** at least one is accepted within 30 days, and hesreallyhim resubmission is made correctly via issue template within 45 days.

### Story 3: Show HN validation
As the maintainer, I want to submit a Show HN post that reaches 30+ points, so that I validate the methodology angle resonates with developers before investing in longer-form content.

**GIVEN** the repo is at least 30 days old and has 10+ stars,
**WHEN** I submit a Show HN using the methodology framing (not the "I built a plugin" framing),
**THEN** the submission reaches 30+ points OR generates 5+ substantive comments about the methodology — confirming the intellectual angle works.

### Story 4: Organic GitHub discovery
As a developer searching GitHub for Claude Code multi-agent tools, I want to find Agent Triforce in search results, so that the repo grows without requiring the maintainer to actively promote it in every channel simultaneously.

**GIVEN** the repo has correct topics, a clear description, and a README with the right keywords,
**WHEN** a developer searches "claude code multi-agent", "claude code checklist", or "claude code pm dev qa",
**THEN** Agent Triforce appears on the first page of GitHub search results for at least one of those queries.

---

## Scope

### In Scope
- Pre-launch readiness checklist (what must be true before any promotion)
- Curated list resubmission strategy with specific timing and framing for each list
- Content marketing sequencing: Show HN → Reddit → Twitter/X → YouTube
- Community building: GitHub Discussions, Product Hunt timing
- Organic SEO/discovery tactics (GitHub topics, README keywords, README structure)
- Metrics and milestones with honest timelines for a solo maintainer
- Lessons learned from the hesreallyhim PR closure applied to all future submissions

### Out of Scope
- Detailed monetization strategy (already covered in `docs/specs/plugin-promotion-plan.md`)
- Feature development roadmap (already covered in `docs/specs/feature-roadmap.md`)
- Paid advertising (not appropriate at current stage)
- Hiring or team expansion
- Partnership deals with newsletters or MCP server creators (Phase 4+ territory, covered in promotion plan)

---

## Non-Functional Requirements

- Every action in this plan must be executable by one person with no budget
- All content links must use UTM parameters from day 1 (even before a formal tracker exists, manual UTM tagging takes 30 seconds)
- No promotion wave may happen before the install path is verified on a clean machine
- All curated list submissions must follow each repo's documented submission process exactly — no shortcuts

---

## Data Requirements

- **Input**: Current repo state (stars, forks, age, topics, README quality), PR statuses, show HN timing data, GitHub Insights traffic data
- **Output**: Weekly star count tracking, referral source breakdown from UTM links, curated list acceptance/rejection log
- **Tracking file**: Create `docs/growth-log.md` to record weekly star counts, content published, submissions made, and results — this is the maintainer's single source of truth for what is working

**Privacy**: No user data collected. All tracking is aggregate (star counts, traffic sources). No newsletter until Phase 2.

---

## Business Rules

1. **Do not promote before verifying the install works.** One broken step in the README makes a first-time visitor leave and never return. Test on a clean machine before any content goes out.
2. **Match each platform's submission protocol exactly.** The hesreallyhim PR closure is the proof case. Read CONTRIBUTING.md and the issue templates before submitting anything.
3. **Lead every piece of content with the methodology argument, not the product.** "I applied Gawande's Checklist Manifesto to AI agents" converts better than "I built a multi-agent plugin." The product is the proof of concept, not the pitch.
4. **Do not reframe as something it is not to avoid the orchestrator label.** If a list maintainer deprioritizes orchestrators, submit under a different value angle (e.g., "checklist-driven development methodology tool") but do not misrepresent what it does.
5. **Respect repo age gatekeeping.** The hesreallyhim repo has explicit bias against repos with 0 stars and no commits older than 24 hours. Wait until the repo is at least 30 days old and has 10+ stars before resubmitting there.
6. **Sequence content before Product Hunt.** Product Hunt rewards momentum. Submitting at 5 stars is worse than not submitting. Wait until 300+ stars.
7. **Respond to all GitHub Issues and Discussions within 48 hours** once any content wave goes live. An unanswered issue during the first impression window kills word-of-mouth.
8. **Pick ONE creative hook for the hesreallyhim submission.** The repo owner explicitly said "PICK THE BEST ONE." The best hook is `/simulate-failure` (F19) — it is the most creative, most novel, and most impossible to replicate with a generic orchestrator. Lead with that, not with the full feature list.

---

## Constraints & Assumptions

### Constraints
- Solo maintainer: all actions must be doable in a few hours per week
- Zero budget: no paid advertising, no paid tools beyond free tiers
- Repo is 12 days old as of 2026-02-26 — gating events (hesreallyhim resubmission, Show HN) must wait for age + social proof
- Plugin marketplace distribution depends on Anthropic's infrastructure remaining stable

### Assumptions
- ccplugins and buildwithclaude are maintained repos that will eventually review open PRs (no evidence of abandonment)
- The Show HN methodology angle will outperform the "I built a tool" angle for this specific audience
- GitHub Discussions is sufficient for community at current scale (no need for Discord until 500+ stars)
- `/simulate-failure` (F19) is the strongest creative differentiator for curated list gatekeepers who value novelty over completeness

---

## Dependencies

- **ccplugins PR #46**: Already open, no action needed except monitoring
- **buildwithclaude PR #67**: Already open, no action needed except monitoring
- **Demo video**: Must be produced before Product Hunt launch and before hesreallyhim resubmission (show, don't tell)
- **Install verification**: Must happen before any content goes live (blocks Show HN)
- **Repo age (30 days)**: Blocks hesreallyhim resubmission — earliest viable date: 2026-03-14
- **Star count (10+)**: Soft gate on Show HN; hard gate on hesreallyhim resubmission
- **GitHub Sponsors setup**: Already in place (FUNDING.yml committed)

---

## Risks & Rollback

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ccplugins and buildwithclaude PRs never reviewed (abandoned repos) | Medium | Medium | Close PRs after 60 days with no activity; pivot to other lists; treat them as low-priority wins, not blocking gates |
| hesreallyhim resubmission rejected again (orchestrator category bias) | Medium | Low | Frame as "checklist-driven development methodology" not "orchestrator." Lead exclusively with `/simulate-failure`. Accept rejection gracefully — this list is not the only channel |
| Show HN underperforms (< 15 points) | Medium | Medium | Retry once 4 weeks later with different title angle. If second attempt also underperforms, skip HN and invest that energy in Reddit and direct newsletter outreach instead |
| Repo stays at < 10 stars after 30 days | Low-Medium | High | Means organic discovery is broken. Run an honest README audit: is the value proposition clear in the first 100 words? Is the install one command? Fix before any further content |
| Plugin install command breaks due to Anthropic marketplace change | Low | High | Maintain manual install fallback in README at all times. Check install command monthly |
| No time to execute — plan sits unused | High | High | Accept only ONE action item per week. This plan is not a sprint. It is a 6-month cadence. Do less, finish it, move to the next thing |

**Rollback criteria**: If after 3 months the repo has fewer than 50 stars and no curated list acceptances, stop active promotion entirely. The problem is the product positioning or the product itself, not the channel selection. Reassess the core value proposition before investing further.

---

## Open Questions

1. Has the install command been tested on a completely clean machine recently? This is the highest-priority unknown before any content goes live.
2. What is the ccplugins maintainer's typical review timeline? Are there any recent accepted PRs that show activity?
3. Is `/simulate-failure` (F19) fully functional and demonstrable in a 2-minute recording? This is the planned creative hook for hesreallyhim.
4. Does the README currently show the methodology value proposition in the first screen (above the fold, before any scrolling)? If not, this is a pre-launch fix, not a later concern.
5. Is there a GitHub Insights baseline recorded? Traffic data from week 1 will be lost if not exported.

---

## Appendix A: Pre-Launch Checklist (READ-DO before any promotion)

These are gates. Nothing ships until all are checked.

- [ ] Install command tested on a clean machine: `gh clone`, fresh Claude Code session, `/plugin marketplace add ArtemioPadilla/agent-triforce`, run `/feature-spec test` — end to end with no errors
- [ ] README shows the methodology argument in the first 200 words (before install instructions)
- [ ] README includes a GIF or screenshot of the workflow in action
- [ ] All 8 GitHub topics verified as applied: `claude-code`, `multi-agent`, `developer-tools`, `prompt-engineering`, `checklist`, `claude-code-plugin`, `code-review`, `security-audit`
- [ ] GitHub description is sharp and under 100 characters — current: "3-agent development system (PM/Dev/QA) with checklist methodology. Install as a Claude Code plugin or use as a project template." (117 chars — trim it)
- [ ] CHANGELOG.md is current and readable as a standalone document (linked from README)
- [ ] `/code-health` scan run; all critical findings resolved; any warnings acknowledged in TECH_DEBT.md
- [ ] `docs/growth-log.md` created with baseline entry (date, star count, fork count, open PRs)

---

## Appendix B: Curated List Resubmission Strategy

### hesreallyhim/awesome-claude-code — Status: CLOSED (PR #819)

**Root cause of closure**: Wrong submission method (PR instead of issue), and the repo owner expressed fatigue with orchestrator submissions.

**When to resubmit**: No earlier than 2026-03-14 (repo 30 days old) AND when star count is 10+.

**How to resubmit**:
1. Use the issue template — do NOT submit a PR. The automated system accepts issues from users; PRs are only from Claude.
2. Frame as a **methodology tool**, not an orchestrator. The angle: "A Claude Code plugin that applies Boeing's checklist engineering and the WHO Surgical Safety Model to multi-agent workflows."
3. Lead exclusively with `/simulate-failure` (F19) as the creative hook. This is the one thing a generic orchestrator cannot claim. The Non-Normal procedure training feature is novel, methodology-rooted, and non-obvious. It passes the "build something that it would not occur to me to ask Claude to build" test.
4. Do NOT submit a wall of features. Submit one thing, the most creative thing, and link to the README for the rest.
5. Include a 60-second demo GIF or Loom link showing `/simulate-failure` in action. Show, do not tell.

**Draft issue title**: "Agent Triforce: Boeing-style Non-Normal procedure training for Claude Code agents (`/simulate-failure`)"

**Draft issue body** (keep under 150 words):
> Agent Triforce applies Boorman's Boeing checklist engineering and the WHO Surgical Safety Model to multi-agent Claude Code workflows. The standout feature is `/simulate-failure` — a Non-Normal procedure training mode that injects simulated failures (broken builds, security findings, conflicting specs) to validate that agents respond correctly using their READ-DO emergency checklists.
>
> It is not an orchestrator in the "many agents doing many things" sense. It is a discipline framework: 3 agents (PM/Dev/QA), 24 checklists, 117 items, zero checklist longer than 9 items (per Boorman's rules). The methodology is the product.
>
> Install: `/plugin marketplace add ArtemioPadilla/agent-triforce`
> Repo: https://github.com/ArtemioPadilla/agent-triforce
> Demo: [link to /simulate-failure Loom]

**Fallback**: If rejected again, do not resubmit. Accept it and move on. This list is a nice-to-have, not a critical path.

---

### ccplugins/awesome-claude-code-plugins — Status: OPEN (PR #46)

**Action needed**: None immediately. PR is open and correctly submitted.

**Follow-up**: If no activity after 30 days (by 2026-03-23), post a brief, respectful comment on the PR: "Hi, checking in on this submission — happy to make any changes if the format doesn't match requirements."

**Do not**: Resubmit, spam, or open a new PR. Wait.

---

### davepoon/buildwithclaude — Status: OPEN (PR #67)

**Action needed**: None immediately. PR is open and correctly submitted.

**Follow-up**: Same as ccplugins — if no activity by 2026-03-23, leave a polite check-in comment.

**Note**: This repo accepted a large `additions: 539` PR which suggests they accept detailed submissions. If they come back with change requests, respond within 48 hours.

---

### Other Lists to Target (after Phase 0 is complete)

| List | Submission Method | Notes | Priority |
|------|-------------------|-------|----------|
| `sindresorhus/awesome` | Issue template | High bar — requires meaningful usage, not just existence. Target after 500 stars. | Low |
| Anthropic official directory | Form submission at `clau.de/plugin-directory-submission` | Unknown review process. Submit in Phase 1. | Medium |
| `claudemarketplaces.com` | Auto-crawled | Monitor within 72 hours of any traffic spike. | Low |
| `github.com/topics/claude-code` | Organic (repo topics already applied) | Already done. | Done |

---

## Appendix C: Content Marketing Sequence

**Rule**: Do not run parallel campaigns. Run one, observe results, run the next.

### Step 1: Show HN (Week 3-4, after pre-launch checklist complete)

**Timing**: Tuesday or Wednesday, 9-11am US Eastern. Do not post on Mondays (buried) or Fridays (low traffic).

**Title options** (test with mental simulation — which would YOU click?):
- Primary: "Show HN: I applied Boeing's checklist engineering to Claude Code agents"
- Backup: "Show HN: What Atul Gawande's Checklist Manifesto taught me about multi-agent AI systems"
- Avoid: "Show HN: I built a 3-agent Claude Code plugin" (generic, no hook)

**Body structure** (keep under 300 words):
1. The problem: AI agents know what to do but skip steps under pressure — this is ineptitude, not ignorance (Gawande's distinction)
2. The analogy: The WHO Surgical Safety Checklist reduced surgical deaths 47% not by teaching surgeons, but by making them confirm they had not forgotten what they already knew
3. The implementation: SIGN IN / TIME OUT / SIGN OUT pause points for PM, Dev, and QA agents — 24 checklists, 117 items, none longer than 9 items
4. The creative hook: `/simulate-failure` injects broken builds and security alerts to verify agents respond correctly
5. The link and install command

**If it gets 30+ points**: Immediately crosspost to Reddit the next day.
**If it gets < 15 points**: Wait 4 weeks, revise the title, retry once. If second attempt also fails, skip HN.

---

### Step 2: Reddit — r/ClaudeAI and r/ClaudeCode (48 hours after Show HN)

**Do not post before Show HN results are in.** HN credibility ("as featured on Hacker News") converts on Reddit.

**r/ClaudeAI title**: "I implemented the WHO Surgical Safety Model for Claude Code agents — here's what SIGN IN / TIME OUT / SIGN OUT looks like on a real feature"

**r/ClaudeCode title** (same angle, slightly more technical): "Agent Triforce: 3 Claude Code agents (PM/Dev/QA) coordinated through Boeing-style checklists — open source and installable in one command"

**Post format**: Text post with 3-4 paragraphs. Do NOT open with "I built X." Open with the problem. Include a GIF or screenshot. End with install command.

**r/LocalLLaMA**: Only if the Show HN performs well and there is genuine LLM methodology interest. This subreddit cares about model behavior, not tooling. The `/simulate-failure` angle (testing agent reliability) fits better here than the general multi-agent pitch.

---

### Step 3: Twitter/X Thread (1 week after Reddit)

**Structure**: 8 tweets.
1. Hook: "Atul Gawande proved that checklists reduce surgical deaths not by teaching surgeons — but by stopping them from skipping what they already knew. I applied this to Claude Code agents."
2. The ineptitude/ignorance distinction (Gawande quote paraphrase)
3. The WHO model: SIGN IN / TIME OUT / SIGN OUT
4. How it maps to PM → Dev → QA workflow
5. Screenshot of a real SIGN IN checklist execution
6. The Non-Normal angle: `/simulate-failure` — what happens when you inject a broken build mid-workflow
7. The numbers: 3 agents, 6 skills, 24 checklists, 117 items
8. Install command + link. Ask: "What other checklist methodologies would you apply to AI agents?"

**Target accounts to tag** (check if they are active before tagging): Anthropic developer relations account, AI coding newsletter writers if any are on X.

---

### Step 4: YouTube/Loom Demo (Month 2)

**Required before**: Product Hunt launch, hesreallyhim resubmission.

**Video structure** (8-10 minutes):
- 0:00–1:30 — The problem: why AI agents repeat the same mistakes
- 1:30–3:00 — The Gawande/Boeing methodology explained (with a whiteboard or slides)
- 3:00–7:00 — Live demo: one complete feature from `/feature-spec` through `/implement-feature` through `/security-audit`, with all SIGN IN / TIME OUT / SIGN OUT checkpoints visible
- 7:00–8:30 — `/simulate-failure` demo: inject a broken build, show Forja's Non-Normal checklist response
- 8:30–9:30 — Install command and getting started

**Platform**: YouTube primary (SEO value). Loom secondary (embed in README and issues).

**Title**: "Boeing-Style Checklists for Claude Code Agents — Agent Triforce Demo"

---

## Appendix D: Organic Growth Tactics

### GitHub Discovery (Do Now — Free, Permanent Value)

- Verify all 8 topics are applied. Current state: `checklist`, `claude-code`, `claude-code-plugin`, `code-review`, `developer-tools`, `multi-agent`, `prompt-engineering`, `security-audit` — already applied.
- Trim the repo description to under 100 characters with a stronger hook. Current: "3-agent development system (PM/Dev/QA) with checklist methodology. Install as a Claude Code plugin or use as a project template." — Proposed: "Claude Code agents with Boeing-style safety checklists. PM + Dev + QA. One install." (86 chars)
- Add a website link in the GitHub repo header pointing to the README or a landing page when it exists.
- Pin the repo to the ArtemioPadilla GitHub profile.
- Add a social preview image (GitHub Open Graph). The current default (no image) is invisible in social sharing.

### README SEO (Do Now)

The README is the primary SEO surface. Developers search GitHub, Google, and community posts. Make sure these phrases appear naturally in the README:
- "claude code multi-agent"
- "checklist methodology"
- "WHO surgical safety checklist"
- "PM dev QA workflow"
- "Gawande" and "Boeing" (these are unique search terms with low competition)

### Boy Scout Rule for Issues

The first person to file a GitHub Issue is a potential advocate. Respond within 24 hours regardless of whether the issue is a bug, question, or feature request. Thank them for being early.

---

## Appendix E: Metrics and Milestones

### Weekly Cadence (Maintainer Action)
Every Monday, record in `docs/growth-log.md`:
- Current star count and delta from last week
- Fork count
- GitHub Insights: unique visitors, clones, top referring sites
- Any curated list updates (accepted/rejected)
- Any content published in the past week

### Milestone Gates

| Milestone | Trigger | Next Action Unlocked |
|-----------|---------|----------------------|
| Repo 30 days old + 10 stars | 2026-03-14 (age) + stars | hesreallyhim issue submission |
| 50 stars | Star count | Show HN submission (if not done already) |
| Show HN 30+ points | HN score | Reddit crosspost |
| 100 stars | Star count | Loom/YouTube demo production begins |
| 200 stars | Star count | hesreallyhim resubmission if not yet accepted |
| 300 stars | Star count | Product Hunt launch preparation |
| Demo video published | Content complete | Product Hunt launch |
| 500 stars | Star count | GitHub Discussions formally opened, seeded |

### Honest Timeline (Solo Maintainer)

These are realistic estimates, not aspirational targets:

| Milestone | Realistic Date | Optimistic Date |
|-----------|---------------|-----------------|
| Pre-launch checklist complete | 2026-03-05 | 2026-02-28 |
| Show HN submission | 2026-03-12 | 2026-03-05 |
| 50 stars | 2026-04-01 | 2026-03-15 |
| hesreallyhim resubmission | 2026-03-25 | 2026-03-14 |
| Demo video published | 2026-04-15 | 2026-04-01 |
| 200 stars | 2026-05-01 | 2026-04-15 |
| Product Hunt launch | 2026-05-15 | 2026-05-01 |
| 500 stars | 2026-07-01 | 2026-06-01 |

---

*Spec authored by Prometeo (PM) — 2026-02-26*
*Complements: `docs/specs/plugin-promotion-plan.md` (monetization and phase strategy)*
*Complements: `docs/specs/feature-roadmap.md` (product features)*
*Next review: 2026-03-26 (30-day check-in)*

# Feature: Agent Triforce — Future Roadmap (Working Backwards, 25-Year Horizon)
**Status**: Approved
**Priority**: P1-High
**Date**: 2026-03-05
**Tier**: L
**Owner**: Prometeo (PM)
**Next Review**: 2026-06-05

---

## Executive Summary

Agent Triforce is an 18-day-old Claude Code plugin with 1 star, 0 forks, and version 0.5.0. It implements a 3-agent PM/Dev/QA system governed by 24 checklists derived from Gawande's *Checklist Manifesto* and Boeing's checklist engineering (Boorman).

The core thesis: **AI agents know what to do. They still skip steps. That is ineptitude, not ignorance — and checklists are the proven answer.** This distinction, first made by Gawande, is the intellectual moat that no competitor can claim retroactively.

This document plans 25 years of product evolution using Amazon's Working Backwards methodology. Each time horizon begins with a press release describing what has been achieved — customer benefit first, product second — then lists the concrete goals that must be true to make that press release accurate. Every goal is tagged by category: [PRODUCT], [GROWTH], [ECONOMICS], [METHODOLOGY], [ECOSYSTEM], or [CHORE].

**The long arc**: Plugin (2026) → Methodology standard (2028) → Industry practice (2031) → Foundational principle of AI-assisted development (2036+).

**Realism principle**: Near-term horizons (through 6 months) are written as operational plans. Mid-term horizons (6 months–3 years) are directional with named uncertainties. Far-term horizons (5+ years) are visionary with explicit speculation markers. Planning does not become less valuable at distance — it becomes a different kind of thinking.

---

## Realism Boundary

| Horizon | Planning Type | Confidence |
|---------|--------------|------------|
| Now – 6 months | Operational plan | High |
| 6 months – 2 years | Strategic direction | Medium |
| 2 years – 5 years | Scenario planning | Low |
| 5 years – 10 years | Visionary thesis | Speculative |
| 10 years – 25 years | Long-range hypothesis | Highly Speculative |

**Why plan past 5 years at all?** Because the methodology thesis either proves true or it does not. If checklist-driven coordination is genuinely the right answer to AI agent reliability, the 25-year arc is coherent. If it is not, the pivot signal will arrive in the first 18 months — long before the speculative horizons become relevant. Planning to 25 years is not forecasting; it is a commitment test. It asks: do we believe this thesis enough to describe a world where it won?

---

## Problem Statement

Agent Triforce solves a specific, documented failure mode in AI-assisted development: agents with sufficient capability to succeed still fail because they skip steps under pressure, lose context across sessions, and lack structured coordination protocols. This is Gawande's ineptitude problem applied to software development tooling.

**For whom**: Individual developers and engineering teams using Claude Code who want structured, reliable, auditable AI-assisted workflows — and who are willing to trade some spontaneity for consistency.

**Evidence of demand**: Multi-agent systems with 73–126 agents exist and have meaningful traction. None use a checklist-based safety methodology. The market for structured AI coordination exists; the methodology angle is unclaimed.

---

## Glossary

- **Working Backwards**: Amazon's product planning methodology: write the press release first, then figure out what must be true to make it accurate
- **Ineptitude failure**: Gawande's term for failures caused by not applying what you already know (vs. ignorance failures from lacking knowledge). The target failure mode for this product.
- **SIGN IN / TIME OUT / SIGN OUT**: The three mandatory pause points borrowed from the WHO Surgical Safety Checklist, adapted for agent workflows
- **Non-Normal procedure**: Boeing's term for emergency checklists activated when standard procedures fail — implemented as `/simulate-failure` in Agent Triforce
- **Pivot trigger**: A specific, pre-defined event or signal that would cause us to abandon or radically change direction before a review date
- **Feedback calibration**: The process of adjusting goals based on observed user behavior and market signals, as opposed to internal planning assumptions

---

## Success Metrics

### Primary KPI: Methodology Adoption (not star count)

Stars are a proxy. The real metric is whether the methodology is being used to ship real features in real projects. Secondary signals:
- GitHub forks (someone is actually using it, not just starring)
- `docs/growth-log.md` entries from third-party contributors
- Consulting inquiries that reference the methodology by name (not just "I want multi-agent AI")
- Citations in blog posts, talks, or papers

### Phase-by-Phase Primary KPIs

| Phase | Primary KPI | Target | Measurement |
|-------|-------------|--------|-------------|
| Now (March 2026) | Pre-launch readiness | 100% checklist complete | Manual checklist in growth-plan.md |
| 1 Month | GitHub stars | 50 | GitHub |
| 3 Months | Active community signal | 10+ GitHub Discussions threads | GitHub |
| 6 Months | Revenue initiation | First paying consulting client | Invoice |
| 12 Months | Methodology recognition | 5 external references (posts/talks) | Manual tracking |
| 2 Years | Platform independence | Works on 2+ AI platforms | Integration count |
| 3 Years | Enterprise adoption | 3+ enterprise clients | Contract count |
| 5 Years | Industry standard signal | Referenced in 1+ industry paper or RFC | Citation tracking |

---

## User Stories

### Story 1: The individual developer who wants structure
As a developer who has been burned by AI agents that hallucinate confidently and skip steps, I want a workflow system that enforces discipline before it asks for creativity, so that I can trust my AI-assisted development pipeline to be consistent — not just occasionally brilliant.

**GIVEN** I install Agent Triforce and run `/feature-spec hello world`,
**WHEN** the PM agent (Prometeo) completes its SIGN IN checklist and writes the spec,
**THEN** I see exactly which decisions were made and why — not just an output, but an auditable trace.

### Story 2: The engineering team lead who needs to justify AI tooling
As an engineering team lead evaluating AI development tools, I want a methodology-backed system I can present to my CTO with documented failure-mode handling, so that I can adopt AI-assisted development with organizational credibility rather than as an experimental bet.

**GIVEN** I am presenting an AI tooling proposal to my organization,
**WHEN** I describe Agent Triforce's methodology foundation (Gawande + Boeing + WHO),
**THEN** I have a credible, documented rationale that answers "what happens when the AI makes a mistake" with a specific answer, not a shrug.

### Story 3: The methodology researcher who studies AI coordination
As a researcher studying multi-agent AI system reliability, I want a reference implementation of checklist-driven agent coordination, so that I can study, extend, and cite a system built on validated human-safety methodology rather than ad-hoc prompt engineering.

**GIVEN** I am writing a paper on AI agent coordination failure modes,
**WHEN** I search for existing implementations of safety-methodology-driven AI agents,
**THEN** Agent Triforce appears as a citable, open-source reference implementation with documented methodology derivation.

---

## Scope

### In Scope
- 14 time-horizon press releases using Working Backwards methodology
- Categorized goals per horizon ([PRODUCT], [GROWTH], [ECONOMICS], [METHODOLOGY], [ECOSYSTEM], [CHORE])
- Confidence level and feedback calibration notes per horizon
- Pivot triggers per horizon
- Category balance analysis per horizon
- Realism boundary section
- Feedback loop design

### Out of Scope
- Feature-level implementation details (covered in `docs/specs/feature-roadmap.md`)
- Tactical growth tactics (covered in `docs/specs/growth-plan.md`)
- Monetization mechanics (covered in `docs/specs/plugin-promotion-plan.md`)
- This document does not replace those specs — it provides the strategic frame that makes them coherent

---

## Non-Functional Requirements

- Every press release must be written customer-first (user benefit, not feature description)
- Near-term goals (through 6 months) must be actionable by a solo maintainer with zero budget
- Far-term visions (5+ years) must be logically derivable from the core methodology thesis
- No goal may be untagged
- Confidence levels must be honest — optimism is welcome; overconfidence destroys planning credibility
- This document must be reviewed quarterly and updated when reality diverges from the plan

---

## Data Requirements

- **Input**: star count, fork count, GitHub traffic, consulting inquiry log, community discussion count, external references
- **Output**: quarterly roadmap review with variance analysis against goals
- **Tracking**: `docs/growth-log.md` (weekly stars/forks), quarterly strategic review in this document's update history
- **Privacy**: all planning data is internal and public (open source); no user PII involved in roadmap planning

---

## Business Rules

1. The methodology thesis is non-negotiable until proven wrong. Goals may be adjusted; the Gawande/Boeing/WHO intellectual foundation is the product identity.
2. Every horizon's goals must be achievable by the team size appropriate to that horizon (solo today; small team at 2 years; potentially larger at 5+ years).
3. A goal that cannot be measured is not a goal — it is a wish. Every goal must have a named measurement method.
4. Near-term goals (through 6 months) must be reviewed monthly. Mid-term (6 months–2 years) quarterly. Far-term annually.
5. When a pivot trigger fires, document the reason and the new direction before abandoning the current plan. Never pivot without a written rationale.
6. The open core model (MIT license, free base) is preserved at every horizon unless a specific business event makes it untenable and a documented decision is made to change it.

---

## Constraints & Assumptions

### Constraints
- Solo maintainer with limited hours through at least 6 months
- Zero budget for paid promotion or infrastructure at current stage
- Claude Code platform dependency — if Anthropic changes the plugin architecture, distribution strategy must adapt
- Anthropic's trust and safety policies govern what agent behaviors are permissible

### Assumptions
- Claude Code (or equivalent AI IDE integration) remains a viable platform through at least 2027
- The checklist methodology angle has genuine market resonance — this is the highest-uncertainty assumption and must be tested by Month 2 (Show HN, Reddit)
- The open source model generates enough awareness to fund consulting and enterprise work
- AI-assisted development becomes mainstream in enterprise software teams by 2028 (if it does not, the addressable market shrinks)
- The distinction between "AI agent with structure" and "AI agent without structure" will matter to at least a segment of the market

---

## Dependencies

- `docs/specs/feature-roadmap.md` — feature implementation sequencing
- `docs/specs/growth-plan.md` — near-term promotion tactics
- `docs/specs/plugin-promotion-plan.md` — monetization mechanics
- Claude Code platform stability (external, not controllable)
- AI development adoption rate (market dependency, not controllable)
- Open source community reception (market dependency, observable via signals)

---

## Risks & Rollback

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Methodology angle does not resonate (core thesis wrong) | Medium | Critical | Show HN + Reddit by Month 2 is the validation test. If < 20 points/upvotes with no methodology comments, reassess positioning before Month 3. |
| Claude Code platform deprioritized by Anthropic | Low | High | Keep the methodology and agent configs portable. The value is in the system prompt files, not the platform hook. |
| AI agent tooling commoditizes faster than expected | Medium | High | Accelerate methodology content output. Establish thought leadership before commoditization. A commodity cannot own an intellectual argument. |
| Solo maintainer burnout | High | Medium | Scope each horizon to solo-maintainer capacity. Never let the plan become a guilt list. |
| Competitor adopts identical methodology framing | Medium | Low | The moat is execution quality and publication date, not IP. Already published. |
| Enterprise AI tooling budgets freeze (macro) | Low-Medium | Medium | Consulting revenue is the first signal. If consulting inquiries stop, enterprise will be harder. |

**Rollback criteria**: If at the 3-month review (June 5, 2026), the repo has fewer than 30 stars, zero consulting inquiries, and no accepted curated list submissions — stop all promotion and do a full positioning audit. The plan fails fast or succeeds fast. Three months is enough signal.

---

## Open Questions

1. Will Anthropic build a native multi-agent orchestration layer that makes the methodology less differentiated? Monitor Anthropic announcements monthly.
2. Is the target persona primarily individual developers (faster to convert, lower revenue per user) or engineering teams (slower to convert, higher revenue)? The first 10 consulting inquiries will answer this.
3. Does the methodology generalize beyond Claude Code to other AI IDEs (Cursor, Windsurf, GitHub Copilot)? If yes, platform independence becomes a major strategic lever.
4. Is "Agent Triforce" a trademark concern with Nintendo's Triforce IP? Legal review needed before any enterprise contracts.
5. What is the right moment to bring in a second contributor? Too early creates coordination overhead; too late creates bottleneck risk.

---

---

# Time Horizons

---

## Horizon 1: NOW (March 5–12, 2026)
**Confidence**: High | **Planning Type**: Operational

### Press Release

*San Francisco, March 12, 2026* — Agent Triforce launches to the developer community with a fully verified installation path, a polished README, and its first curated list submission in review. Developers who follow the install instructions reach their first working agent workflow in under 10 minutes, with no broken steps. "I expected another half-baked AI agent template," says one early user from r/ClaudeCode. "The methodology section in the README actually made me understand why this is different."

### Goals This Week

| # | Goal | Category | Owner | Done? |
|---|------|----------|-------|-------|
| 1 | Verify install command works end-to-end on a clean machine | [CHORE] | Solo | [ ] |
| 2 | README shows methodology argument in first 200 words (above fold) | [PRODUCT] | Solo | [ ] |
| 3 | Trim GitHub description to under 100 characters with a stronger hook | [GROWTH] | Solo | [ ] |
| 4 | Confirm all 8 GitHub topics are applied | [GROWTH] | Solo | [ ] |
| 5 | Add social preview image (GitHub Open Graph) | [GROWTH] | Solo | [ ] |
| 6 | Create `docs/growth-log.md` with baseline entry (stars: 1, forks: 0) | [CHORE] | Solo | [ ] |
| 7 | Run `/code-health` scan; resolve any critical findings | [CHORE] | Solo | [ ] |
| 8 | Pin repo to ArtemioPadilla GitHub profile | [GROWTH] | Solo | [ ] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 4 | [ECONOMICS]: 0 | [METHODOLOGY]: 0 | [ECOSYSTEM]: 0 | [CHORE]: 3

### Feedback Calibration
This week is pre-launch preparation. Success is binary: either the install works and the README is polished, or it is not. No external feedback expected. Internal signal: does the SIGN OUT checklist for all pre-launch items pass?

### Pivot Triggers
- If the install command is fundamentally broken and requires architecture changes, delay all promotion until resolved. Do not promote a broken install.

---

## Horizon 2: 1 WEEK (March 12, 2026)
**Confidence**: High | **Planning Type**: Operational

### Press Release

*San Francisco, March 12, 2026* — Agent Triforce submits to Hacker News Show HN with a methodology-first framing. Within 24 hours, the post has generated substantive discussion about the Gawande/Boeing angle applied to AI agents — the first public validation that the intellectual hook resonates with developers. "I never thought about AI agent failures as ineptitude vs. ignorance until I read this," writes a top commenter. The repo doubles its star count in 48 hours.

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | Submit Show HN post: "I applied Boeing's checklist engineering to Claude Code agents" (Tuesday or Wednesday, 9-11am ET) | [GROWTH] |
| 2 | Pre-launch checklist 100% complete before submission | [CHORE] |
| 3 | Repo age: 18 days — note for hesreallyhim gate (needs 30 days) | [CHORE] |
| 4 | Monitor ccplugins PR #46 and buildwithclaude PR #67 | [GROWTH] |
| 5 | Respond to every HN comment within 2 hours on day of submission | [GROWTH] |
| 6 | Record HN result in growth-log.md within 24 hours | [CHORE] |

### Category Balance
- [PRODUCT]: 0 | [GROWTH]: 4 | [ECONOMICS]: 0 | [METHODOLOGY]: 0 | [ECOSYSTEM]: 0 | [CHORE]: 2

### Feedback Calibration
**Signal A (positive)**: Show HN reaches 30+ points with methodology comments. Proceed to Reddit crosspost within 48 hours.
**Signal B (neutral)**: 15-30 points, no methodology comments. The hook works for engagement but the intellectual angle is not the draw. Revise framing for Reddit.
**Signal C (negative)**: Under 15 points. Hypothesis: the methodology angle may not be the first hook. Consider leading with `/simulate-failure` as the creative hook instead. Retry in 3 weeks.

### Pivot Triggers
- If Show HN and retry both score under 15 points, abandon HN as a channel. Pivot budget of time to direct newsletter outreach and Discord communities.

---

## Horizon 3: 1 MONTH (April 5, 2026)
**Confidence**: High | **Planning Type**: Operational

### Press Release

*San Francisco, April 5, 2026* — Agent Triforce reaches 50 GitHub stars one month after its first public promotion, with two curated list submissions accepted and active developer discussions on Reddit and GitHub. Three developers have submitted issues requesting industry-specific checklist customizations, signaling organic product demand beyond the initial audience. "I forked it and configured it for my fintech team's compliance workflow in an afternoon," reports a developer on r/ClaudeCode. "The checklist structure made customization obvious."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 50 GitHub stars | [GROWTH] |
| 2 | At least 1 curated list accepted (ccplugins or buildwithclaude) | [GROWTH] |
| 3 | Reddit posts live on r/ClaudeAI and r/ClaudeCode | [GROWTH] |
| 4 | hesreallyhim issue submitted (repo turns 30 days old ~March 14) | [GROWTH] |
| 5 | At least 1 GitHub Discussion thread seeded and active | [GROWTH] |
| 6 | Twitter/X thread published | [GROWTH] |
| 7 | `docs/growth-log.md` has 4 weekly entries | [CHORE] |
| 8 | Install command re-verified after any README changes | [CHORE] |
| 9 | First consulting landing page drafted (even if not published) | [ECONOMICS] |
| 10 | Respond to all issues within 48 hours | [CHORE] |

### Category Balance
- [PRODUCT]: 0 | [GROWTH]: 6 | [ECONOMICS]: 1 | [METHODOLOGY]: 0 | [ECOSYSTEM]: 0 | [CHORE]: 3

### Feedback Calibration
**Key question**: Is the GitHub fork count growing? Stars are passive; forks are active. Even 3-5 forks at 50 stars would be a healthy signal. Zero forks at 50 stars means people are interested but not using it.

**Adjustment trigger**: If Reddit posts generate 0 comments about methodology and all engagement is "cool plugin" — reconsider whether the methodology angle is the right lead. Test a more technical, implementation-focused framing.

### Pivot Triggers
- If at 1 month: 0 forks, 0 curated list acceptances, 0 issues filed by strangers → positioning audit required. The product exists but is not compelling enough to use.

---

## Horizon 4: 3 MONTHS (June 5, 2026)
**Confidence**: High | **Planning Type**: Operational

### Press Release

*San Francisco, June 5, 2026* — Agent Triforce surpasses 150 GitHub stars and receives its first consulting inquiry from an engineering team at a fintech company seeking to implement checklist-driven AI workflows. The methodology, once an abstract intellectual argument, has demonstrated concrete demand from practitioners. "We've been burned by AI agents that confidently skip steps," says the team lead. "Knowing there's a Boeing-derived protocol underneath changes how we think about adopting this." The project has delivered on its promise: structure out of chaos, even with short context windows.

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 150 GitHub stars | [GROWTH] |
| 2 | Product Hunt preparation started (300 stars gate for launch) | [GROWTH] |
| 3 | First consulting inquiry received and responded to within 48 hours | [ECONOMICS] |
| 4 | Demo video published (YouTube/Loom, 8-10 minutes) | [GROWTH] |
| 5 | GitHub Sponsors setup live with 3 tiers | [ECONOMICS] |
| 6 | At least 10 active GitHub Discussions threads | [GROWTH] |
| 7 | Substack newsletter launched (3 issues published) | [GROWTH] |
| 8 | At least 2 curated list acceptances total | [GROWTH] |
| 9 | hesreallyhim submission result known (accepted or final rejection) | [GROWTH] |
| 10 | v0.6.0 release with at least 1 user-requested improvement | [PRODUCT] |
| 11 | Consulting offer defined and priced (landing page or README section) | [ECONOMICS] |
| 12 | Quarterly roadmap review: update this document with actual vs. planned | [CHORE] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 7 | [ECONOMICS]: 3 | [METHODOLOGY]: 0 | [ECOSYSTEM]: 0 | [CHORE]: 1

### Feedback Calibration
**Consulting inquiry signal**: One consulting inquiry at 3 months = the market exists. Zero inquiries at 150 stars = the audience is interested but not decision-makers. Adjust content toward team leads rather than individual developers.

**Star quality signal**: Are the stars coming from developers who open issues, fork, or discuss? Or are they passive? GitHub Insights referral data will show if stars are coming from curated lists, HN, Reddit, or organic search — each tells a different story about which channel to invest in.

### Pivot Triggers
- If demo video gets under 100 views in 30 days, YouTube is not a viable channel. Redirect to Loom embeds in targeted community posts.
- If Substack grows to 50+ subscribers but generates zero consulting inquiries, the newsletter audience is curious but not buyers. Shift content to practical implementation guides rather than methodology theory.

---

## Horizon 5: 6 MONTHS (September 5, 2026)
**Confidence**: High | **Planning Type**: Operational/Strategic

### Press Release

*San Francisco, September 5, 2026* — Agent Triforce reaches 500 GitHub stars and closes its first paying consulting engagement. A fintech engineering team reports a measurable reduction in AI-assisted development incidents after implementing the SIGN IN / TIME OUT / SIGN OUT protocol across their workflows. The project launches on Product Hunt, reaching the top 10 tools of the day. Revenue exceeds $1,000 in its first month of active consulting. "This is the first AI development tool I've been able to explain to my CISO," says the CTO of a mid-size SaaS company. "The checklist methodology gives it an audit trail that nothing else has."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 500 GitHub stars | [GROWTH] |
| 2 | Product Hunt launch (top 10 product of the day) | [GROWTH] |
| 3 | First consulting engagement closed ($1,500–$5,000) | [ECONOMICS] |
| 4 | $1,000+ total revenue (sponsors + consulting + digital products) | [ECONOMICS] |
| 5 | GitHub Sponsors: at least 5 active sponsors | [ECONOMICS] |
| 6 | At least 1 conference CFP submitted | [METHODOLOGY] |
| 7 | First v1.0.0 release (stable API, versioned agents) | [PRODUCT] |
| 8 | Industry checklist pack for 1 vertical (fintech or healthcare) | [ECONOMICS] |
| 9 | At least 3 external blog posts or videos referencing the methodology | [GROWTH] |
| 10 | Cross-promotion partnership with at least 1 complementary plugin creator | [ECOSYSTEM] |
| 11 | `docs/growth-log.md` has 26 weekly entries with trend data | [CHORE] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 5 | [ECONOMICS]: 4 | [METHODOLOGY]: 1 | [ECOSYSTEM]: 1 | [CHORE]: 1

### Feedback Calibration
**Revenue composition signal**: If consulting > 80% of revenue at 6 months, diversification is needed before Month 9. Consulting-heavy revenue means the product is a service, not a product. Accelerate digital product sales.

**Community signal**: Are third-party developers customizing and sharing their configurations? The first "I adapted this for X workflow" GitHub Discussion or blog post is a milestone indicator that the methodology is transferable.

### Pivot Triggers
- If Product Hunt scores under 100 upvotes: the audience is real but small. Narrow focus to B2B (team leads) rather than B2C (individual devs). Change all content positioning accordingly.
- If first consulting engagement ends in dissatisfaction: pause all consulting until root cause is identified and delivery process is improved.

---

## Horizon 6: 9 MONTHS (December 5, 2026)
**Confidence**: Medium | **Planning Type**: Strategic

### Press Release

*San Francisco, December 5, 2026* — Agent Triforce ends its first year with 1,500 GitHub stars, an active developer community, and $5,000+ monthly revenue across sponsors, consulting, and digital products. The methodology has been cited in two developer conference talks and a widely-read AI engineering post. Enterprise inquiries have begun arriving from teams that need not just a plugin but a documented AI development governance framework. "We've been looking for something to put in our AI development policy document," says a VP of Engineering at a Series B startup. "Agent Triforce's methodology is the first thing I've found that could actually go into a compliance framework."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 1,500 GitHub stars | [GROWTH] |
| 2 | $5,000+ monthly recurring revenue (sponsors + products + consulting retainer) | [ECONOMICS] |
| 3 | At least 2 conference talks or invited methodology discussions | [METHODOLOGY] |
| 4 | First enterprise inquiry (company with 50+ developers) | [ECONOMICS] |
| 5 | v1.1.0 release with community-contributed improvements | [PRODUCT] |
| 6 | At least 1 third-party contributor with merged PR | [GROWTH] |
| 7 | Industry checklist packs for 2+ verticals | [ECONOMICS] |
| 8 | Substack newsletter: 500+ subscribers, 40%+ open rate | [GROWTH] |
| 9 | Platform exploration started: does the methodology work in Cursor or Windsurf? | [ECOSYSTEM] |
| 10 | Tech debt audit and cleanup sprint | [CHORE] |
| 11 | First methodology white paper or long-form post (3,000+ words) | [METHODOLOGY] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 4 | [ECONOMICS]: 3 | [METHODOLOGY]: 2 | [ECOSYSTEM]: 1 | [CHORE]: 1

### Feedback Calibration
**Enterprise signal**: Are enterprise inquiries asking about customization, compliance documentation, or SLAs? If customization: they want a product. If compliance docs: they want a framework. If SLAs: they want a vendor. Each requires a different response strategy.

**Community signal**: The first externally-originated PR is a qualitative milestone. When does it arrive? The longer it takes, the more the project is a solo author's tool rather than a community standard.

### Pivot Triggers
- If no enterprise inquiries by December 2026, the B2B thesis may be wrong for the current product state. Refocus on individual developer experience and viral growth rather than enterprise sales.
- If no community contributors by Month 9, the contribution barriers are too high. Simplify the methodology templates, add a "how to contribute a checklist" guide, and create `good first issue` labels.

---

## Horizon 7: 12 MONTHS (March 5, 2027)
**Confidence**: Medium | **Planning Type**: Strategic

### Press Release

*San Francisco, March 5, 2027* — Agent Triforce celebrates its first year with 3,000 GitHub stars, two enterprise clients, and $30,000 in annual revenue. The project has been featured in three major AI engineering publications and cited in an academic paper on multi-agent AI system reliability. The methodology has moved from a plugin's README to a reference document cited by practitioners building AI development governance policies. "One year ago I thought 'checklist-driven AI development' sounded like over-engineering," writes a senior developer on their blog. "One year later, I cannot imagine building a serious AI development workflow without it."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 3,000 GitHub stars | [GROWTH] |
| 2 | 2 enterprise clients ($10,000+ annual contract each) | [ECONOMICS] |
| 3 | $30,000 total first-year revenue | [ECONOMICS] |
| 4 | Cited in at least 1 academic or industry research paper | [METHODOLOGY] |
| 5 | v2.0.0 release: methodology stabilized, agent API versioned | [PRODUCT] |
| 6 | At least 5 external contributors with merged PRs | [GROWTH] |
| 7 | Works on at least 2 AI platforms (Claude Code + one other) | [ECOSYSTEM] |
| 8 | Methodology white paper published and indexed | [METHODOLOGY] |
| 9 | Team grows: at least 1 regular contributor or paid part-time collaborator | [GROWTH] |
| 10 | Annual revenue > hosting + time cost: product is economically sustainable | [ECONOMICS] |
| 11 | First retrospective published: what worked, what did not, what we changed | [METHODOLOGY] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 4 | [ECONOMICS]: 3 | [METHODOLOGY]: 3 | [ECOSYSTEM]: 1 | [CHORE]: 0

### Feedback Calibration
**Academic citation signal**: If cited in research, the methodology claim is being treated as a scholarly contribution. This opens university partnerships, conference keynotes, and a different class of enterprise conversation.

**Revenue composition signal**: By Year 1, if consulting accounts for more than 70% of revenue, the product has not achieved product-market fit for digital goods. The right answer at Year 1 is 40% consulting / 30% digital products / 20% enterprise / 10% sponsors.

### Pivot Triggers
- If revenue at 12 months is under $10,000 total, reassess the commercial thesis. The methodology may be valuable but not monetizable at current scale. Either grow the audience faster or reduce the commercial ambition and treat it as a community project.

---

## Horizon 8: 2 YEARS (March 2028)
**Confidence**: Low | **Planning Type**: Scenario Planning

### Press Release

*San Francisco, March 2028* — Agent Triforce 3.0 launches as the first methodology-certified AI development framework, with 10,000+ GitHub stars and a growing ecosystem of third-party plugins and vertical-specific checklist packs. Five companies have published case studies describing measurable reliability improvements from implementing the SIGN IN / TIME OUT / SIGN OUT protocol. The framework now runs on three AI development platforms. "I recommended Agent Triforce to my entire engineering organization," says the CTO of a 200-person software company. "It is the only AI development framework with a documented answer to the question 'what happens when the AI is wrong?'"

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 10,000 GitHub stars | [GROWTH] |
| 2 | Framework runs on 3+ AI platforms (platform-agnostic methodology layer) | [ECOSYSTEM] |
| 3 | 5 published customer case studies with quantitative reliability data | [METHODOLOGY] |
| 4 | Enterprise clients: 10+ companies with formal engagements | [ECONOMICS] |
| 5 | $150,000+ annual revenue | [ECONOMICS] |
| 6 | Third-party checklist pack ecosystem (5+ community-contributed packs) | [ECOSYSTEM] |
| 7 | v3.0 architecture: methodology as a library, not just agent configs | [PRODUCT] |
| 8 | Dedicated contributor team (3–5 core contributors) | [GROWTH] |
| 9 | First methodology certification or training program | [METHODOLOGY] |
| 10 | Conference keynote or invited talk at a major AI engineering event | [METHODOLOGY] |
| 11 | Academic partnership (university research collaboration) | [METHODOLOGY] |

### Category Balance
- [PRODUCT]: 1 | [GROWTH]: 3 | [ECONOMICS]: 2 | [METHODOLOGY]: 4 | [ECOSYSTEM]: 2 | [CHORE]: 0

### Feedback Calibration
**Platform signal**: Which platform adopts the methodology fastest? Individual developers on VS Code/Cursor, or enterprise teams on GitHub Copilot? The answer defines the 3-year distribution strategy.

**Ecosystem signal**: Are third parties building on the methodology without being asked? Unsolicited community contributions, blog posts teaching the methodology, and independent certifications are the clearest signals that the methodology has escaped its origin.

### Pivot Triggers
- [SPECULATIVE] If a major AI platform (GitHub Copilot, Cursor) natively implements a similar checklist protocol, the plugin distribution model is threatened. Pivot to methodology consulting and certification rather than tool distribution.

---

## Horizon 9: 3 YEARS (March 2029)
**Confidence**: Low | **Planning Type**: Scenario Planning

### Press Release

*San Francisco, March 2029* — Agent Triforce methodology becomes the de facto reference framework for AI agent reliability in software development, with 30,000+ GitHub stars, a formal certification program with 200+ certified practitioners, and integration into 5 major AI development platforms. Three engineering-focused universities have incorporated the checklist methodology into their AI engineering courses. "The difference between an AI development team that uses Agent Triforce and one that doesn't is the same as the difference between a hospital that uses the WHO checklist and one that doesn't," writes an industry analyst in a widely-cited report. "One is trying to be reliable. The other is hoping to be."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | 30,000 GitHub stars | [GROWTH] |
| 2 | Formal certification program: "Certified Agent Triforce Practitioner" | [METHODOLOGY] |
| 3 | 200+ certified practitioners | [METHODOLOGY] |
| 4 | Integrated into 5 major AI development platforms | [ECOSYSTEM] |
| 5 | University adoption: 3+ courses referencing the methodology | [METHODOLOGY] |
| 6 | $500,000+ annual revenue | [ECONOMICS] |
| 7 | Published book or formal specification document | [METHODOLOGY] |
| 8 | Open governance model (foundation or steering committee) | [GROWTH] |
| 9 | Annual "Checklist-Driven AI Development" conference or summit | [METHODOLOGY] |
| 10 | Government or regulated-industry adoption (fintech, healthcare, defense) | [ECOSYSTEM] |

### Category Balance
- [PRODUCT]: 0 | [GROWTH]: 3 | [ECONOMICS]: 1 | [METHODOLOGY]: 5 | [ECOSYSTEM]: 2 | [CHORE]: 0

**Note**: By Year 3, product maintenance is table stakes. The strategic investment shifts entirely to methodology validation and ecosystem expansion.

### Feedback Calibration
**Regulation signal**: Is any government or standards body (NIST, ISO, ENISA) discussing AI agent reliability frameworks? If yes, Agent Triforce's documented methodology positions it for standards-track participation.

**Practitioner signal**: Are certified practitioners finding jobs specifically because of their certification? Employment market signals (job postings asking for "checklist-driven AI development" experience) indicate the methodology has crossed into professional credential territory.

### Pivot Triggers
- [SPECULATIVE] If LLMs achieve reliable self-correction without external structure (the "reasoning models solve ineptitude" scenario), the checklist methodology's value proposition weakens. Pivot to higher-level governance frameworks and human-AI collaboration protocols that remain relevant even with more capable models.

---

## Horizon 10: 5 YEARS (March 2031)
**Confidence**: Speculative | **Planning Type**: Visionary Thesis

### Press Release

*San Francisco, March 2031* — Agent Triforce's checklist methodology has become a foundational principle of AI-assisted software development, referenced in ISO standards, taught in 50+ university programs, and implemented by 1,000+ organizations worldwide. The framework, which began as a Claude Code plugin, is now a platform-agnostic specification that any AI development tool can implement. A new generation of developers has never known AI-assisted development without SIGN IN / TIME OUT / SIGN OUT discipline. "Asking whether to use a checklist methodology for AI agents is like asking whether to use version control," says a software engineering professor at MIT. "The question has been answered. The only question is which implementation."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | ISO or equivalent standard published with Agent Triforce methodology as reference | [METHODOLOGY] |
| 2 | 50+ university programs teaching the methodology | [METHODOLOGY] |
| 3 | 1,000+ organizations using the methodology (certified or self-reported) | [GROWTH] |
| 4 | Platform-agnostic methodology specification (not tied to any AI vendor) | [ECOSYSTEM] |
| 5 | Foundation or nonprofit governing the standard | [METHODOLOGY] |
| 6 | $2M+ annual revenue (products + licensing + certification + events) | [ECONOMICS] |
| 7 | Annual report on AI agent reliability in software development | [METHODOLOGY] |
| 8 | Companion methodology for AI agents in non-software domains (medical, legal, financial) | [ECOSYSTEM] |

### Category Balance
- [PRODUCT]: 0 | [GROWTH]: 2 | [ECONOMICS]: 1 | [METHODOLOGY]: 5 | [ECOSYSTEM]: 2 | [CHORE]: 0

### Feedback Calibration
**Standards signal**: Has any national or international standards body (NIST AI RMF, ISO/IEC JTC 1) referenced the methodology in a formal document? This is the primary signal that the methodology has moved from community consensus to formal standard.

### Pivot Triggers
- [HIGHLY SPECULATIVE] If AI agents become sufficiently autonomous that human-structured coordination protocols are no longer relevant (full autonomy), the methodology may need to evolve into AI-to-AI protocol design rather than human-to-AI workflow design. The intellectual core (ineptitude failures require structural remediation, not more capability) may still apply in that world — but the implementation will look entirely different.

---

## Horizon 11: 10 YEARS (March 2036)
**Confidence**: Highly Speculative | **Planning Type**: Long-Range Hypothesis

### Press Release

*San Francisco, March 2036* — A decade after its release as a Claude Code plugin, the Agent Triforce methodology is now an industry standard for AI agent reliability across software, healthcare, finance, and government. The 2026 insight — that AI agents fail not from lack of capability but from lack of discipline, and that checklists are the proven remedy — is cited as a foundational contribution to the field of AI engineering. What began as three agents (PM, Dev, QA) governed by 24 checklists has evolved into a universal framework for structured human-AI and AI-AI collaboration. "The Gawande-Boorman approach to AI reliability is now what TDD was to software quality in the 2000s," says a technology historian. "It took a decade to become standard practice. Now nobody argues about it."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | Methodology cited as foundational in AI engineering curriculum globally | [METHODOLOGY] |
| 2 | Cross-domain adoption: healthcare, legal, financial, government AI workflows | [ECOSYSTEM] |
| 3 | Second-generation methodology: AI-to-AI coordination protocols | [METHODOLOGY] |
| 4 | Open standard maintained by a multi-stakeholder foundation | [METHODOLOGY] |
| 5 | Research institute or chair in "Structured AI Collaboration" methodology | [METHODOLOGY] |
| 6 | Annual reliability benchmark for AI development tools using the methodology | [METHODOLOGY] |

### Category Balance
- [METHODOLOGY]: 5 | [ECOSYSTEM]: 1 | All others: 0

**Note**: At this horizon, the "product" is the methodology. The software implementation is maintained by the community; the strategic focus is on the intellectual framework's evolution.

### Feedback Calibration
At 10 years, the feedback signal is historical: did the thesis prove correct? The measure is not star count but intellectual influence — citations, standards references, practitioner count, and whether the next generation of AI developers learns the methodology as foundational knowledge.

### Pivot Triggers
- [HIGHLY SPECULATIVE] If AI reasoning capabilities advance to the point where structured protocols are no longer needed (AGI-level reliability), the methodology's role shifts from "required practice" to "historical contribution." The intellectual argument remains valid as an explanation of why AI development became reliable — even if future systems no longer need external structure to achieve that reliability.

---

## Horizon 12: 15 YEARS (March 2041)
**Confidence**: Highly Speculative | **Planning Type**: Long-Range Hypothesis

### Press Release

*San Francisco, March 2041* — The Gawande-Boorman-Triforce methodology for AI agent coordination has been adopted by the United Nations Technology Governance body as the reference framework for AI system reliability in critical infrastructure. What began as a checklist for a Claude Code plugin now governs AI systems in hospitals, financial markets, and government services across 40 countries. "Structure out of chaos" — the design principle articulated in 2026 — has become the defining philosophy of responsible AI deployment. A new academic discipline, "AI Coordination Science," traces its origins to the insight that AI agents, like surgeons, need checklists not because they lack knowledge, but because consistent execution under pressure requires structure.

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | International regulatory adoption in at least one critical infrastructure domain | [ECOSYSTEM] |
| 2 | "AI Coordination Science" recognized as a distinct sub-discipline | [METHODOLOGY] |
| 3 | 10,000+ organizations globally using certified methodology implementations | [GROWTH] |
| 4 | Methodology extended to AI-to-AI coordination without human intermediaries | [METHODOLOGY] |
| 5 | Foundational textbook: "Structured AI Development — Theory and Practice" | [METHODOLOGY] |

### Category Balance
- [METHODOLOGY]: 3 | [ECOSYSTEM]: 1 | [GROWTH]: 1

### Feedback Calibration
At 15 years, the primary signal is whether the methodology has transcended its software development origin and been applied in other domains where AI agent reliability matters. Medical AI coordination, financial AI governance, and government AI decision-making are the test cases.

---

## Horizon 13: 20 YEARS (March 2046)
**Confidence**: Highly Speculative | **Planning Type**: Long-Range Hypothesis

### Press Release

*San Francisco, March 2046* — Twenty years after a developer applied Atul Gawande's Checklist Manifesto to a Claude Code plugin, the core insight has become a principle of information science: **structured coordination protocols improve outcomes in any system where components (human or AI) are capable but prone to skipping steps under pressure.** The methodology has been formalized in mathematics, proven in controlled studies across domains from surgery (where it began) to AI engineering to autonomous system governance. "We now understand that ineptitude failures are not a defect of intelligence," writes a leading AI scientist. "They are a feature of any capable system operating under resource constraints. Structure is not a crutch — it is the architecture of reliability."

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | Formal mathematical theory of structured coordination protocols published | [METHODOLOGY] |
| 2 | Cross-domain validation studies: AI, medicine, law, autonomous systems | [METHODOLOGY] |
| 3 | "Ineptitude failure" recognized as a formal category in AI systems science | [METHODOLOGY] |
| 4 | Agent Triforce Foundation: a nonprofit endowment sustaining the open standard | [ECONOMICS] |
| 5 | Methodology adapted for post-human-mediated AI coordination (AI agent-only teams) | [METHODOLOGY] |

### Category Balance
- [METHODOLOGY]: 4 | [ECONOMICS]: 1

---

## Horizon 14: 25 YEARS (March 2051)
**Confidence**: Highly Speculative | **Planning Type**: Legacy Hypothesis

### Press Release

*San Francisco, March 2051* — A quarter century after its founding, Agent Triforce's core contribution — that reliable AI development requires structural discipline, not just technical capability — is recognized as a foundational insight of the AI age. The WHO Surgical Safety Checklist reduced surgical deaths 47% not by making surgeons smarter, but by ensuring they never skipped what they already knew. The equivalent reduction in AI development failures, documented across millions of deployments over 25 years, has validated the thesis beyond any reasonable doubt. "We didn't make AI more capable," says the founder of Agent Triforce at a retrospective conference. "We made it more consistent. And consistency, it turns out, was worth more than capability." The methodology is now taught in every software engineering program in the world, not as a tool, but as a principle.

### Goals

| # | Goal | Category |
|---|------|----------|
| 1 | "Structured AI development" recognized as a universal engineering principle (like TDD, CI/CD) | [METHODOLOGY] |
| 2 | The core thesis — ineptitude failures require structural remediation, not more capability — validated by 25 years of adoption data | [METHODOLOGY] |
| 3 | Open standard maintained by a multi-generational community, no longer dependent on any single organization or platform | [METHODOLOGY] |
| 4 | Agent Triforce's role as the origin of the standard documented in technology history | [METHODOLOGY] |
| 5 | The methodology's benefits are measurable across every domain it was applied to (software, healthcare, legal, government, autonomous systems) | [METHODOLOGY] |

### Category Balance
- [METHODOLOGY]: 5

**Note**: At 25 years, the entire roadmap has collapsed into a single question: Was the thesis true? Every other metric — stars, revenue, features, platforms — is instrumental. The thesis is the destination.

---

---

# Category Balance Summary

The following table shows goal distribution across all 14 horizons, highlighting the strategic shift from execution to methodology leadership.

| Horizon | [PRODUCT] | [GROWTH] | [ECONOMICS] | [METHODOLOGY] | [ECOSYSTEM] | [CHORE] |
|---------|-----------|----------|-------------|---------------|-------------|---------|
| Now (Week) | 1 | 4 | 0 | 0 | 0 | 3 |
| 1 Week | 0 | 4 | 0 | 0 | 0 | 2 |
| 1 Month | 0 | 6 | 1 | 0 | 0 | 3 |
| 3 Months | 1 | 7 | 3 | 0 | 0 | 1 |
| 6 Months | 1 | 5 | 4 | 1 | 1 | 1 |
| 9 Months | 1 | 4 | 3 | 2 | 1 | 1 |
| 12 Months | 1 | 4 | 3 | 3 | 1 | 0 |
| 2 Years | 1 | 3 | 2 | 4 | 2 | 0 |
| 3 Years | 0 | 3 | 1 | 5 | 2 | 0 |
| 5 Years | 0 | 2 | 1 | 5 | 2 | 0 |
| 10 Years | 0 | 0 | 0 | 5 | 1 | 0 |
| 15 Years | 0 | 1 | 0 | 3 | 1 | 0 |
| 20 Years | 0 | 0 | 1 | 4 | 0 | 0 |
| 25 Years | 0 | 0 | 0 | 5 | 0 | 0 |

**Key observation**: The roadmap begins as an execution plan ([GROWTH] + [CHORE] dominant) and ends as a methodology legacy ([METHODOLOGY] dominant). The transition begins at Month 6 when methodology goals appear alongside economics. By Year 2, methodology investment overtakes growth investment. This shift is deliberate: the product achieves its purpose when the methodology becomes larger than the product.

---

---

# Feedback Loop

The plan adjusts based on observed signals. This section defines the calibration mechanism.

## Signal Collection (Weekly)

Every Monday, record in `docs/growth-log.md`:
- Star count and weekly delta
- Fork count and weekly delta
- GitHub Insights: unique visitors, clones, top referral sources
- Content published in the past week
- Community activity: issues opened, Discussions posts, external mentions

## Signal Collection (Monthly)

First Monday of each month:
- Consulting inquiry count and pipeline status
- Revenue summary (sponsors + products + consulting)
- External references (blog posts, talks, papers citing the methodology)
- Curated list status updates

## Plan Adjustment Rules

| Signal | Adjustment |
|--------|-----------|
| Stars growing 50%+ faster than plan | Accelerate content and Product Hunt timeline |
| Stars growing 50%+ slower than plan | Positioning audit before next content wave |
| First consulting inquiry arrives early | Pull forward enterprise goals by one horizon |
| Zero forks at 50+ stars | The audience is passive; revise content strategy to target practitioners, not enthusiasts |
| Community PR arrives unsolicited | Contribution infrastructure must be ready; add `CONTRIBUTING.md`, `good first issue` labels |
| External methodology citation received | Begin white paper and conference CFP immediately |
| No methodology comments on content | The intellectual angle is not landing; test a more practical, implementation-focused framing |
| Enterprise inquiry before 500 stars | Reassess B2B timing; enterprise may be faster than the individual developer path |
| Revenue > costs before 12 months | Reinvest surplus in contributor compensation, not infrastructure |

## Quarterly Strategic Review

Every 90 days (June 5, September 5, December 5, March 5):
1. Update this document with actual vs. planned metrics for all goals in the elapsed horizons
2. Identify which goals were achieved, which were missed, and why
3. Adjust the next horizon's goals based on variance
4. Update MEMORY.md with key strategic learnings
5. Identify if any pivot triggers have fired

The quarterly review is the primary mechanism for keeping this document honest. A roadmap that is never updated against reality is not a roadmap — it is a wish list.

---

---

# Phased Delivery

| Phase | Scope | Acceptance Criteria | Target Date |
|-------|-------|---------------------|-------------|
| Phase 0: Pre-launch | Install verified, README polished, growth log started | 100% pre-launch checklist complete | March 12, 2026 |
| Phase 1: Soft launch | Show HN, Reddit, curated lists | 50 stars, 1 list accepted, 1 methodology discussion | April 5, 2026 |
| Phase 2: Content momentum | Demo video, newsletter, consulting offer | 150 stars, first inquiry, Substack live | June 5, 2026 |
| Phase 3: Community | Product Hunt, GitHub Discussions, v1.0 | 500 stars, first revenue, 10+ discussions | September 5, 2026 |
| Phase 4: Authority | Talks, enterprise, methodology white paper | 1,500 stars, $5K MRR, 2 talks | December 5, 2026 |
| Phase 5: Legitimacy | 3K stars, enterprise clients, academic citation | $30K annual revenue, platform expansion | March 5, 2027 |
| Phase 6: Platform | Platform-agnostic methodology, 10K stars | 3 platforms, certification program | March 2028 |
| Phase 7: Standard | ISO/standards reference, 30K stars | University adoption, foundation governance | March 2029 |
| Phase 8: Principle | Methodology as universal AI engineering principle | Global adoption, multiple domain validation | March 2031+ |

---

# Interface / API Contract

This document does not define a software API. It defines the **strategic contract** between the roadmap and execution:

1. Every horizon review must produce a written update documenting variance and rationale
2. Every pivot trigger activation must produce a written decision log entry
3. Every new horizon's goals must be validated against the previous horizon's outcomes
4. Category balance must be checked at each quarterly review — if [METHODOLOGY] goals are behind their expected growth trajectory by Year 2, strategic investment must shift

---

# Migration & Backward Compatibility

**Near-term (through 6 months)**: No breaking changes. The methodology's agent configs, skills, and checklist format must remain stable. Users who install today must not need to reconfigure in 30 days.

**Mid-term (Year 1–2)**: v2.0.0 may introduce breaking changes to the agent API if necessary for platform independence. Migration guides required. The methodology itself (Gawande/Boeing/WHO) never changes — only the technical implementation.

**Long-term (Year 3+)**: When the methodology becomes platform-agnostic, the Agent Triforce brand may be associated with the specification rather than the implementation. "Built on Agent Triforce methodology" becomes the value, not "uses the Agent Triforce plugin."

---

# Testing Strategy

This is a strategic planning document, not a software feature. Its "tests" are the feedback signals and pivot triggers defined above. However, the following verification applies:

- **Unit test**: Each horizon's goals are independently verifiable (measurable, named measurement method). Run this check quarterly.
- **Integration test**: Goals across horizons are logically derivable from each other. A gap at Horizon 4 should not make Horizon 5 impossible. Run this check at each quarterly review.
- **E2E test**: The 25-year arc makes sense as a coherent narrative. Does Month 1 success lead plausibly to Year 1 success, which leads plausibly to Year 5? Run annually.
- **Regression test**: When goals are adjusted at quarterly review, do the adjustments preserve the core thesis? Never adjust the methodology thesis as a response to short-term metric shortfalls.

---

# Story Map / Dependency Graph

```
Thesis: Ineptitude failures in AI agents require structural remediation
    |
    v
Plugin (2026) ──── [GROWTH] Distribution ──── [ECONOMICS] Revenue
    |                                              |
    v                                              v
Methodology (2027) ── [METHODOLOGY] White Paper ── Enterprise (2027)
    |
    v
Platform-Agnostic (2028) ──── [ECOSYSTEM] Multi-platform
    |
    v
Standard (2029) ──── [METHODOLOGY] Certification ──── University
    |
    v
Principle (2031+) ──── [METHODOLOGY] ISO / Foundation
    |
    v
Legacy (2041-2051): "Ineptitude failures" as a formal scientific category
```

**Critical path**: Thesis validation (Show HN + Reddit by April 2026) → Community signal (forks + discussions by June 2026) → Methodology authority (talks + white paper by December 2026) → Platform independence (2028) → Standard (2029) → Principle (2031+).

Every horizon depends on the previous one's thesis validation. If the thesis fails in the first 3 months, no subsequent horizon is relevant. This is correct — it is not a flaw in the plan. A plan that acknowledges its own killswitch is honest about its uncertainty.

---

*Authored by Prometeo (PM) — 2026-03-05*
*Method: Amazon Working Backwards (press release first, then goals)*
*Intellectual foundation: Gawande (ineptitude vs. ignorance), Boeing/Boorman (checklist engineering), WHO (SIGN IN / TIME OUT / SIGN OUT)*
*Complements: `docs/specs/feature-roadmap.md` (product features), `docs/specs/growth-plan.md` (growth tactics), `docs/specs/plugin-promotion-plan.md` (monetization)*
*Next review: 2026-06-05*

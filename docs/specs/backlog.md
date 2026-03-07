# Backlog

Living intake document for work items. Each item gets promoted to a spec (`docs/specs/`) or resolved in-place.

## Format

```
### [B-NNN] Title
- **Type**: Bug | Feature | Chore | Research
- **Category**: [PRODUCT] | [GROWTH] | [ECONOMICS] | [METHODOLOGY] | [ECOSYSTEM] | [CHORE]
- **Priority**: P0 | P1 | P2 | P3
- **Owner**: Prometeo | Forja | Centinela | Solo
- **AC**: One-line acceptance criterion
- **Status**: Open | In Progress | Done | Promoted to spec
```

## Open

### [B-005] Social preview image for GitHub Open Graph
- **Type**: Chore
- **Category**: [GROWTH]
- **Priority**: P1
- **Owner**: Solo
- **AC**: Repo shows a branded preview image when shared on social media
- **Status**: Open

### [B-006] Pin repo to GitHub profile
- **Type**: Chore
- **Category**: [GROWTH]
- **Priority**: P2
- **Owner**: Solo
- **AC**: ArtemioPadilla GitHub profile shows agent-triforce as a pinned repo
- **Status**: Open

### [B-009] MkDocs Material documentation site
- **Type**: Feature
- **Category**: [GROWTH]
- **Priority**: P1
- **Owner**: Forja
- **AC**: `mkdocs serve` renders a polished docs site with landing page, quickstart, agent reference, skills catalog, workflow diagrams, and changelog. Deployed to GitHub Pages via `gh-pages` branch.
- **Status**: Open
- **Notes**: Solves B-005 (social preview — site becomes the shareable link), supports growth plan content marketing, and gives a proper URL for Show HN / Reddit / curated list submissions.

### [B-008] Clean install test on fresh machine
- **Type**: Chore
- **Category**: [CHORE]
- **Priority**: P0
- **Owner**: Solo
- **AC**: Full install → `/agent-triforce:feature-spec test` completes with zero errors on a machine that has never seen the repo
- **Status**: Open
- **Ref**: Growth plan Appendix A gate 1

## Resolved

### [B-001] Suggest possible next steps (brainstorm)
- **Type**: Research
- **Category**: [PRODUCT]
- **Status**: Done (2026-03-05)
- **Resolution**: Created `docs/specs/future-roadmap.md` — 14-horizon strategic plan with Working Backwards press releases

### [B-002] Assess and adjust on user expectations
- **Type**: Research
- **Category**: [PRODUCT]
- **Status**: Done (2026-03-05)
- **Resolution**: Addressed in future-roadmap.md user stories and feedback loop design

### [B-003] Dashboard creates too many new tabs without project name
- **Type**: Bug
- **Category**: [PRODUCT]
- **Status**: Done (2026-03-05)
- **Resolution**: Added `--no-open` flag, updated SubagentStop hook, added project name to title/header. Commit `0044d98`.

### [B-007] Fix session-tracker dead branch (H-1)
- **Type**: Bug
- **Category**: [PRODUCT]
- **Status**: Done (2026-03-05)
- **Resolution**: Fixed `_count_findings()` to attribute findings to correct agent (forja-dev for general reviews, prometeo-pm for business reviews). Also moved `import re` to top-level. Commit `a035e89`.

### [B-004] Dashboard doesn't show requirements or future steps
- **Type**: Bug
- **Category**: [PRODUCT]
- **Status**: Done (2026-03-05)
- **Resolution**: Added AC count badges to pipeline cards, "Next Step" in stats bar, renamed section to "Recommended Next Steps". Commit `0044d98`.

---
type: plan
status: open
created: 2026-10-16
updated: 2026-10-16
linked_from: system_enhancement.md §8
depends_on: edge_cap.md
---

# Scenario run-throughs

## Problem

- The graph is only checked structurally (`build.py`): edges resolve, counts fit, ramps land.
- Nothing checks that a real situation reaches a fitting skill. The two smoke-test crawls at build time each found a fix (e.g. Myths About Emotions was reachable only from a ramp), which suggests more gaps remain.
- Smoke tests are ad hoc: not recorded, not repeatable, not re-run after edits.

## Possible solutions

1. **Scenario fixtures.** A file (e.g. `scenarios.yaml`) of situations, each with the expected ramp and skill(s). `build.py` checks that a path still exists.
2. **Agent crawl.** An agent reads a scenario, crawls from ramps using only page edges, and reports where it lands, dead ends, and links it wanted but couldn't find. Missing links become candidate edges for review.
3. **Coverage sweep.** Generate scenarios aimed at every page; flag pages no scenario reaches and ramps no scenario uses.
4. **A command or skill** that runs 2 (and optionally 3) on demand and writes findings to a log for review.

## Open questions

- Who writes scenarios: AI-generated only, or adapted from real situations? Real ones must be scrubbed of personal details before commit.
- Does the crawling agent see only edges (tests the graph) or also its own DBT knowledge (tests the delivery)?
- How many scenarios is enough, and per module or cross-module?

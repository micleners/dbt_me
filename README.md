# dbt_me

A traversable graph of DBT skill cards. You start from what you're feeling — a felt state, a situation, or a goal — and crawl typed links between skills to reach a concrete suggestion. The chat interface is the crawler today; a web app over the same structured data comes later. **The graph is the product; clients are interchangeable renderers on top of it.**

DBT (Dialectical Behavior Therapy, Marsha Linehan's framework) has four skills modules: Mindfulness, Distress Tolerance, Emotion Regulation, Interpersonal Effectiveness. Card content is sourced from https://dialecticalbehaviortherapy.com and paraphrased into cards — that site *is* the card deck. One page = one card = one node.

## Start here

| File | What it is |
|------|-----------|
| [`SCHEMA.md`](SCHEMA.md) | The data model — nodes, typed edges, ramps, guardrails. Read first. |
| [`CLAUDE.md`](CLAUDE.md) | Project orientation, conventions, and current status. |
| [`methodology/module_fetch.md`](methodology/module_fetch.md) | The 9-step pipeline for building a module + a reusable prompt for the rest. |
| [`methodology/system_enhancement.md`](methodology/system_enhancement.md) | Cross-cutting backlog (new relations, missing ramps, client architecture). |
| [`validation/research-summary.md`](validation/research-summary.md) | External research validating the data model. |

## Layout

```
SCHEMA.md          data model (read first)
build.py           no-dependency validator + backlinks.json generator
ramps.yaml         entry ramps (felt-state / situation / goal)
backlinks.json     generated reverse index (never hand-edited)
cards/<module>/    one card (node + outgoing edges) per file
raw/<module>/       summarized page caches with quoted excerpts (not verbatim; never re-fetched)
methodology/       how a module is built + the enhancement backlog
validation/        data-model validation research
```

## Build

```
python build.py
```

Validates the graph (fails non-zero on a broken intra-module edge, a card outside the 3–6 edge guardrail, or an unresolved ramp target) and regenerates `backlinks.json`. Run it after any card or ramp change.

## Status

- **Distress Tolerance** — complete: 13 cards, 49 edges, 11 ramps, passing `build.py`.
- **Mindfulness · Emotion Regulation · Interpersonal Effectiveness** — not yet built; follow `methodology/module_fetch.md`.

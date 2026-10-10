# CLAUDE.md

Project conventions and orientation for the DBT Skills Web app.

## What this is

A traversable graph of DBT (Dialectical Behavior Therapy) skill "cards" that you crawl from a felt state, situation, or goal toward a concrete skill suggestion. The chat interface is the crawler today; a web app over the same structured data comes later. The structured data is the product — clients (chat, web, an LLM) are interchangeable renderers on top of it.

## Grounding

DBT is Marsha Linehan's framework, organized into four skills modules: **Mindfulness**, **Distress Tolerance**, **Emotion Regulation**, **Interpersonal Effectiveness**. Card content is sourced from https://dialecticalbehaviortherapy.com and paraphrased into cards — that website *is* the card deck for this project. One page = one card = one node.

## Structure

```
SCHEMA.md          Data model: nodes (cards), typed edges, ramps, guardrails. Read this first.
build.py           No-dependency build step: validates the graph, generates backlinks.json.
ramps.yaml         Entry ramps (felt-state / situation / goal) that point into the graph.
backlinks.json     Generated reverse index. Never hand-edited.
cards/<module>/    One Markdown+YAML file per card (node + its outgoing edges).
raw/<module>/      Summarized page dumps with quoted excerpts (not verbatim; permanent fetch cache; never re-fetched).
methodology/       How a module was built + a reusable prompt to build the rest.
validation/        External research validating the data model.
```

**Data vs. delivery.** The graph supplies *which skill and why* (card body + each edge's `note`). The client supplies the empathic, situation-specific *delivery*. Keep that seam clean: don't bake one person's phrasing into a card, and don't let a client invent skills the graph doesn't contain.

## Status

- **Distress Tolerance** — complete: 13 cards (T1–T13), 49 edges, 11 ramps, passing `build.py`.
- **Mindfulness** — complete: 10 cards (M1–M10), 34 edges, 6 ramps, passing `build.py`. Added the `builds_on` relation to `SCHEMA.md`; the cross-module edges Distress Tolerance points at (`mindfulness/wise-mind`, `mindfulness/observing`) now resolve.
- **Emotion Regulation, Interpersonal Effectiveness** — not yet built. See `methodology/module_fetch.md`.

## Workflow

Run `python build.py` after any card or ramp change — it fails non-zero on a broken intra-module edge, a card outside the 3–6 edge guardrail, or an unresolved ramp target.

Always commit and push after completing even a minor task. A "stop here" checkpoint counts as the work coming to rest: whenever you pause, hand back, or are told to stop before the next phase, commit and push whatever is in the working tree first, including intermediate artifacts like a raw fetch cache or a progress note. Do not leave uncommitted changes sitting while you wait for the next instruction. The only reason to hold off is the sensitive-information check below.

Before committing, scan the changed documents for sensitive information about any individuals. If any exists, flag it and hold off. Otherwise, commit and push all uncommitted changes once the work has come to rest.

## Writing conventions

- **Do not force-wrap markdown.** Write paragraphs as single continuous lines and let the editor soft-wrap. Do not insert hard line breaks to hit a column width.

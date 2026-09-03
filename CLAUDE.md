# CLAUDE.md

Project conventions and orientation for the DBT Skills Web app.

## What this is

A traversable graph of DBT (Dialectical Behavior Therapy) skill "cards" that you crawl from a felt state, situation, or goal toward a concrete skill suggestion. The chat interface is the crawler today; a web app over the same structured data comes later. The structured data is the product — clients (chat, web, an LLM) are interchangeable renderers on top of it.

## Grounding

DBT is Marsha Linehan's framework, organized into four skills modules: **Mindfulness**, **Distress Tolerance**, **Emotion Regulation**, **Interpersonal Effectiveness**. Card content is sourced verbatim from https://dialecticalbehaviortherapy.com — that website *is* the card deck for this project. One page = one card = one node.

## Structure

```
SCHEMA.md          Data model: nodes (cards), typed edges, ramps, guardrails. Read this first.
build.py           No-dependency build step: validates the graph, generates backlinks.json.
ramps.yaml         Entry ramps (felt-state / situation / goal) that point into the graph.
backlinks.json     Generated reverse index. Never hand-edited.
cards/<module>/    One Markdown+YAML file per card (node + its outgoing edges).
raw/<module>/      Verbatim page dumps (permanent fetch cache; never re-fetched).
methodology/       How a module was built + a reusable prompt to build the rest.
validation/        External research validating the data model.
```

**Data vs. delivery.** The graph supplies *which skill and why* (card body + each edge's `note`). The client supplies the empathic, situation-specific *delivery*. Keep that seam clean: don't bake one person's phrasing into a card, and don't let a client invent skills the graph doesn't contain.

## Status

- **Distress Tolerance** — complete: 13 cards (T1–T13), 49 edges, 11 ramps, passing `build.py`.
- **Mindfulness, Emotion Regulation, Interpersonal Effectiveness** — not yet built. See `methodology/module_fetch.md`.
- Known follow-up: add a `builds_on` relation (reverse of `prerequisite_of`) when building Mindfulness; it resolves the 5 cross-module edges Distress Tolerance already points at (`mindfulness/wise-mind`, `mindfulness/observing`).

## Workflow

Run `python build.py` after any card or ramp change — it fails non-zero on a broken intra-module edge, a card outside the 3–6 edge guardrail, or an unresolved ramp target.

## Writing conventions

- **Do not force-wrap markdown.** Write paragraphs as single continuous lines and let the editor soft-wrap. Do not insert hard line breaks to hit a column width.

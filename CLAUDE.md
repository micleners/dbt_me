# CLAUDE.md

A traversable graph of DBT (Dialectical Behavior Therapy) skill cards: crawl from a felt state, situation, or goal to a concrete skill. Chat is the crawler today; a web app comes later. The structured data is the product; clients are interchangeable renderers on top of it.

DBT is Marsha Linehan's framework, with four modules: **Mindfulness**, **Distress Tolerance**, **Emotion Regulation**, **Interpersonal Effectiveness**. Cards paraphrase https://dialecticalbehaviortherapy.com: one page = one card = one node.

## Structure

```
SCHEMA.md                     Data model: cards, typed edges, ramps, guardrails. Read first.
build.py                      Validates the graph; generates backlinks.json.
ramps.yaml                    Entry ramps (felt-state / situation / goal) into the graph.
backlinks.json                Generated reverse index. Never hand-edit.
cards/<module>/               One Markdown+YAML card per page: the node and its outgoing edges.
raw/<module>/                 Fetch cache: summarized pages with quoted excerpts, not verbatim. Never re-fetch.
supplemental_dbt_flashcards/  Paraphrased notes on a physical flash card deck; outside the graph until integrated.
methodology/                  How modules are built, plus a reusable build prompt.
validation/                   External research validating the data model.
```

## Status

- **Distress Tolerance:** 13 cards (T1–T13), 49 edges, 11 ramps.
- **Mindfulness:** 10 cards (M1–M10), 34 edges, 6 ramps.
- **Emotion Regulation** (E1–E12), **Interpersonal Effectiveness** (I1–I13): raw pages cached, cards not built. See `methodology/module_fetch.md`.
- **Supplemental deck:** in progress, one file per card as photos arrive.

## Writing card content

Applies to `cards/` and `supplemental_dbt_flashcards/`.

- Stay faithful: keep every step, its order, and any durations; add no steps, benefits, or claims the source doesn't make.
- Paraphrase; don't reuse the source's sentences. Keep fixed names as-is: exercise names, example mantras, acronym letters.
- Use Linehan's terms exactly (wise mind, radical acceptance, willingness, TIPP).
- Keep steps exactly as concrete as the source: no vaguer, no more specific.
- Write in a neutral reference register: describe the skill, don't comfort or persuade.
- Our additions (DBT knowledge, overlap, integration ideas) go in edge `note`s or a `## Notes` section, never in the paraphrase.
- Don't force-wrap markdown: one line per paragraph.

**Supplemental flashcards:** for each deck photo, write `supplemental_dbt_flashcards/<module>/<###>-<card-title>.md` (deck number zero-padded, title in kebab-case) in the format that folder's `README.md` defines, including the `repo_overlap` assessment.

## Delivering skills to a person

The graph supplies *which skill and why* (card body + edge `note`); the client (you, when crawling in chat) supplies the *delivery*. Keep the seam clean: don't bake one person's phrasing into a card, and don't offer skills the graph doesn't contain.

- Describe the person's situation without judgment ("bad," "should," "overreacting").
- Validate first, then offer a skill as something to practice; never promise it will make the feeling go away.
- Fit the warmth and wording to their situation.
- In acute crisis or risk of harm, point to real support (crisis line, emergency services, their clinician) before any card.

The full data-vs-delivery contract is still open: `methodology/system_enhancement.md` §3.

## Workflow

- Run `python build.py` after any card or ramp change. It fails on a broken intra-module edge, a card outside 3–6 edges, or an unresolved ramp target.
- Commit and push whenever work comes to rest, including pauses, hand-backs, and "stop here" checkpoints. Include intermediate artifacts (raw caches, progress notes). Never leave changes uncommitted while waiting.
- Before committing, scan the changes for sensitive information about individuals. If any exists, flag it and hold off.

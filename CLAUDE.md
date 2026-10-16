# CLAUDE.md

A traversable graph of DBT (Dialectical Behavior Therapy) skill pages: crawl from a felt state, situation, or goal to a concrete skill. Chat is the crawler today; a web app comes later. The structured data is the product; clients are interchangeable renderers on top of it.

DBT is Marsha Linehan's framework, with four modules: **Mindfulness**, **Distress Tolerance**, **Emotion Regulation**, **Interpersonal Effectiveness**. Pages paraphrase https://dialecticalbehaviortherapy.com: one source page = one page = one node.

## Structure

```
SCHEMA.md                     Data model: pages, typed edges, ramps, guardrails. Read first.
build.py                      Validates the graph; generates backlinks.json.
ramps.yaml                    Entry ramps (felt-state / situation / goal) into the graph.
backlinks.json                Generated reverse index. Never hand-edit.
pages/<module>/               One Markdown+YAML page per source page: node plus its edges.
raw/<module>/                 Fetch cache: summarized pages with quoted excerpts, not verbatim. Never re-fetch.
supplemental_dbt_flashcards/  Paraphrased notes on a physical flash card deck; outside the graph until integrated.
methodology/                  Backlog, plans, investigations; archive/ holds retired procedures.
.claude/skills/               Agent skills: dbt-conversation (talking with a person), dbt-flashcard-ingest (logging deck cards).
validation/                   External research validating the data model.
```

## Status

- **Distress Tolerance:** 13 pages (T1–T13), 49 edges, 11 ramps.
- **Mindfulness:** 10 pages (M1–M10), 34 edges, 6 ramps.
- **Interpersonal Effectiveness:** 13 pages (I1–I13), 52 edges, 7 ramps.
- **Emotion Regulation:** 12 pages (E1–E12), 46 edges, 8 ramps.
- **Supplemental deck:** in progress, one file per card as photos arrive.

## Writing page content

Applies to `pages/` and `supplemental_dbt_flashcards/`.

- Stay faithful: keep every step, its order, and any durations; add no steps, benefits, or claims the source doesn't make.
- Paraphrase; don't reuse the source's sentences. Keep fixed names as-is: exercise names, example mantras, acronym letters.
- Use Linehan's terms exactly (wise mind, radical acceptance, willingness, TIPP).
- Keep steps exactly as concrete as the source: no vaguer, no more specific.
- Write in a neutral reference register: describe the skill, don't comfort or persuade.
- Our additions (DBT knowledge, overlap, integration ideas) go in edge `note`s or a `## Notes` section, never in the paraphrase.
- Don't force-wrap markdown: one line per paragraph.

**Supplemental flashcards:** ingest deck cards with the `dbt-flashcard-ingest` skill.

## Talking with a person

Conversations that guide someone toward skills follow the `dbt-conversation` skill (`.claude/skills/dbt-conversation/SKILL.md`). Keep the seam: pages hold *which skill and why*; the conversation supplies the delivery.

## Instruction hygiene

Applies to agent-facing files: `CLAUDE.md`, `.claude/skills/`, `methodology/`.

- Write imperative, checkable bullets under headings. No prose paragraphs or run-on sentences.
- Include only what an agent would get wrong without it. Cut generic advice and anything inferable from the repo.
- No history logs, backstory, or meta commentary. History lives in git; open decisions in `methodology/system_enhancement.md`.
- No embellishment. Reserve emphasis (IMPORTANT, bold) for rules that are ignored without it.
- Give each fact one home and point to it; don't restate it across files.
- Put situational procedures in a skill, not here: `CLAUDE.md` loads every session. Keep `CLAUDE.md` under ~200 lines and each `SKILL.md` under ~500; split overflow into reference files.
- Skill `description`s state what the skill does and when to use it.
- When editing these files, prune stale or conflicting lines in the same change.

## Workflow

- Run `python build.py` after any page or ramp change. It fails on a broken intra-module edge, a page outside 3–6 edges, or an unresolved ramp target.
- Commit and push whenever work comes to rest, including pauses, hand-backs, and "stop here" checkpoints. Include intermediate artifacts (raw caches, progress notes). Never leave changes uncommitted while waiting.
- Before committing, scan the changes for sensitive information about individuals. If any exists, flag it and hold off.

---
type: procedure
status: archived
created: 2026-09-02
updated: 2026-10-16
archived: 2026-10-16
reason: All four site modules are built (48 pages). Reuse only if a new source module is added.
---

# Building a module

Per-module build procedure, plus a prompt to run it. Read `SCHEMA.md` first; this doc assumes the data model. Module status lives in `CLAUDE.md`; cross-cutting findings go in `system_enhancement.md`.

## Pipeline

1. **Enumerate the module's pages.** Crawl the module's parent page on https://dialecticalbehaviortherapy.com for every exercise (name + URL). Verify the count against the page DOM or a screenshot; the fetcher's summarizer silently truncates lists.
2. **Record URL quirks.** Capture each page's real URL; some sit outside the module path or are misspelled. Use them verbatim. Known: T2 sits under `/emotional-regulation/`; E11 and E12 sit under `/emotion-regulation/`; I10's slug is `resisitance-and-conflict`.
3. **One source page = one node.** Acronym skills (TIPP, ACCEPTS, DEAR MAN) stay single nodes with their letters in the body; don't split into per-letter children.
4. **Fetch via one haiku sub-agent.**
   - Dispatch ONE `general-purpose` agent on `haiku` to fetch all pages serially into `raw/<module>/<prefix>##-slug.md` (prefix T, M, E, I) with `source_url` + `fetched` frontmatter.
   - Have it return only a manifest: per page, title, one-line summary, in-body links to other exercises.
   - Expect summaries with quoted key lines, not verbatim text; that is enough to paraphrase from.
   - `raw/` is a permanent cache; never re-fetch a cached page. For exact wording, `curl` the HTML instead.
5. **Author pages in the main context, not a sub-agent.** Edges need all pages in view. Write `pages/<module>/<slug>.md` with the frontmatter in `SCHEMA.md` and a distilled body that points to `source_url`.
6. **Derive edges semantically.** In-body site links are mostly module navigation; use them only as corroboration. Enforce 3–6 outbound edges per page, a `note` on every edge, and the most true relation, not the most generic.
7. **Write `ramps.yaml` entries.** `kind: felt-state | situation | goal`, a `cue`, edges in; `primary: true` marks the first suggestion. A gateway page is a ramp target whose own edges do the branching.
8. **Validate.** Run `python build.py` until clean; remove the module from `FUTURE_MODULES` in `build.py`. Edges into unbuilt modules are reported, not errors.
9. **Smoke-test by crawling.** Walk one realistic scenario through the edges to a suggestion. Fix dead ends and mis-fitting hops in the edges.
10. **Update status** in `CLAUDE.md`.

## Prompt

> Build the **`<MODULE>`** module (parent page `<PARENT_URL>`) for dbt_me. Read `CLAUDE.md`, `SCHEMA.md`, and `methodology/archive/module_fetch.md`, then follow the pipeline exactly. Report the enumerated page list and count before fetching; skip fetching if `raw/<module>/` is already populated. Finish with what the smoke-test crawl surfaced and which edges you fixed.

Parent pages:
- Mindfulness: https://dialecticalbehaviortherapy.com/mindfulness/
- Emotion Regulation: https://dialecticalbehaviortherapy.com/emotional-regulation/
- Interpersonal Effectiveness: https://dialecticalbehaviortherapy.com/interpersonal-effectiveness/

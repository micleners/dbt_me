# Building a module

How the **Distress Tolerance** module was built, and a reusable prompt to build the remaining three the same way. Read `SCHEMA.md` first — this doc assumes the data model.

## Progress

- **Distress Tolerance** — complete (13 cards, T1–T13). The original build this doc is written from.
- **Mindfulness** — complete (10 cards, M1–M10, 34 edges, 6 ramps). Added the `builds_on` relation to `SCHEMA.md` and resolved the cross-module edges Distress Tolerance pointed at (`mindfulness/wise-mind`, `mindfulness/observing`). Removed `mindfulness` from `build.py`'s `FUTURE_MODULES`.
- **Emotion Regulation** — in progress. 12 cards (E1–E12). URL quirk: E1–E10 sit under `/emotional-regulation/`, but E11 STOP and E12 ABC PLEASE sit under `/emotion-regulation/` (no "-al"). Raw pages fetched to `raw/emotion-regulation/`; Opus card authoring not yet started.
- **Interpersonal Effectiveness** — in progress. 13 cards (I1–I13). URL quirk: I10's page slug is misspelled `resisitance-and-conflict` (extra "i") on the source site; use it verbatim. Acronym skills: I11 DEAR MAN, I12 FAST, I13 GIVE. Raw pages fetched to `raw/interpersonal-effectiveness/`; Opus card authoring not yet started.

## The pipeline we used

1. **Enumerate the deck.** Crawl the module's parent page on https://dialecticalbehaviortherapy.com to list every exercise (name + URL). Verify the count against a second source (the page DOM or a screenshot) — the fetcher's summarizer silently truncated lists, and the true count came from the DOM. Distress Tolerance = 13 cards (T1–T13), despite an initial guess of 18.

2. **Record URL quirks.** Card URLs don't always sit under the module's path. Example: T2 "Recognize Emotional Crisis" lives under `/emotional-regulation/…` though it is card T2 of Distress Tolerance. Capture the real URL per card.

3. **Fix granularity up front: one page = one card = one node.** Acronym skills (TIPP, ACCEPTS, RESISTT) stay *single* nodes with their letters described in the body — do not split into per-letter children unless traversal later demands it.

4. **Fetch via a single haiku sub-agent.** Dispatch ONE `general-purpose` agent on the `haiku` model to fetch all pages serially and write each to `raw/<module>/T##-slug.md`, with `source_url` + `fetched` frontmatter. **The resulting dumps are not verbatim.** The fetch tool passes each page through a model before the agent sees it, so what lands in `raw/` is a faithful summary with direct quotes for key lines, not the page text: sections are condensed, worked examples are abridged ("*Example provided:* ..."), and worksheets and links are described rather than reproduced. That has been accurate enough to author paraphrased cards from, which is all `raw/` is used for. If exact wording is ever needed, fetch the raw HTML (e.g. `curl`) and convert it to text instead. One agent = one cold start (cheapest) and keeps raw page text out of the orchestrator's context. Have it return only a manifest: per card, title, one-line summary, and in-body links to other exercises. `raw/` is a permanent cache — never re-fetch.

5. **Author cards (orchestrator, not a sub-agent).** Read the raw dumps and write `cards/<module>/<slug>.md`: frontmatter (`id`, `title`, `module`, `card_no`, `source_url`, `type`, `category`, `summary`, `tags`, `when_to_use`, `when_not_to_use`, `edges`) plus a distilled prose body that points to `source_url` for full detail. Do the authoring yourself in the main context — edges are a global problem and need all cards in view.

6. **Derive edges semantically.** The site's in-body links are mostly module navigation (every page links to most others) — noise, not signal. Derive typed edges from the *content* and DBT knowledge; use the curated in-body links only as corroboration. Enforce the guardrails: 3–6 outbound edges per card, a mandatory `note` on every edge, and pick the relation that is *most true*, not the most generic.

7. **Write `ramps.yaml`.** Entry ramps by `kind: felt-state | situation | goal`, each with a `cue` and edges into the graph (`primary: true` marks the first suggestion). A "gateway" card (e.g. Recognize Emotional Crisis) is a ramp target whose own edges do the branching.

8. **Validate + generate.** Run `python build.py`. It writes `backlinks.json` and fails non-zero on a broken intra-module edge, a card outside 3–6, or an unresolved ramp target. Cross-module edges into unbuilt modules are expected and reported separately, not errors.

9. **Smoke-test by crawling.** Feed the finished module a realistic scenario in chat and walk the edges to a suggestion. Dead ends and mis-fitting hops are data — fix the edges, don't paper over them.

Cross-cutting findings from building a module (new relations, missing ramps, client architecture) are tracked in `system_enhancement.md`, not here — this doc stays focused on the per-module procedure.

---

## Reusable prompt — build the next module

> Paste this to a fresh session (or continue an existing one) to build **Mindfulness**, **Emotion Regulation**, or **Interpersonal Effectiveness**. Replace `<MODULE>` and `<PARENT_URL>`.

You are building the **`<MODULE>`** module for the dbt_me project. Read `SCHEMA.md`, `CLAUDE.md`, and `methodology/module_fetch.md` first, then follow the 9-step pipeline in that methodology doc exactly. Specifics:

1. Crawl `<PARENT_URL>` to enumerate every exercise (name + full URL). **Verify the count** against the page DOM or a screenshot before proceeding — do not trust the summarized list alone. Report the list and count back before fetching.
2. Note any card whose URL sits outside the module path.
3. Keep one page = one card; do not split acronym skills into per-letter nodes.
4. Dispatch ONE haiku `general-purpose` sub-agent to fetch all pages serially into `raw/<module-dir>/T##-slug.md` with `source_url` + `fetched` frontmatter (expect summarized dumps with quoted excerpts, not verbatim text), returning only a manifest (title, one-line summary, in-body exercise links).
5. Author each card yourself from the raw dumps, following the frontmatter shape and 3–6 edge / mandatory-`note` guardrails. Derive edges semantically; treat in-body nav links as noise.
6. If this is **Mindfulness**: first add a `builds_on` relation to `SCHEMA.md`'s vocabulary (reverse of `prerequisite_of`), then resolve the cross-module edges Distress Tolerance already points at — `mindfulness/wise-mind`, `mindfulness/observing`, `mindfulness/mindful-breathing` must exist as real card ids (match those exact slugs).
7. Add module-appropriate entries to `ramps.yaml`.
8. Run `python build.py` until it exits clean (no broken intra-module edges, all cards within 3–6, all ramp targets resolve).
9. Smoke-test with one realistic scenario crawl, then report what the crawl surfaced and any edges you had to fix.

Module parent pages (verify each before fetching):
- Mindfulness — https://dialecticalbehaviortherapy.com/mindfulness/
- Emotion Regulation — https://dialecticalbehaviortherapy.com/emotional-regulation/
- Interpersonal Effectiveness — https://dialecticalbehaviortherapy.com/interpersonal-effectiveness/

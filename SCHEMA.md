# DBT Skills Web — Data Model

A directed graph. **Pages are nodes**, **pointers are typed edges**. The edge *type* (and optional condition) is the engine that makes traversal intelligent instead of a flat wiki of backlinks.

Content lives as Markdown + YAML frontmatter so it is human-editable and git-diffable now, and trivially parsed into JSON for any future web/mobile client later.

## Directory layout

```
dbt_me/
  SCHEMA.md                     <- this file
  raw/
    <module>/T##-<page>.md      <- summarized page dump, not verbatim (cache; never re-fetched)
  pages/
    <module>/<page>.md          <- one file per page (node + its outgoing edges)
  ramps.yaml                    <- entry points (felt-state / situation / goal)
  backlinks.json                <- generated reverse index (never hand-edited)
```

Pages are *distilled* from `raw/`. A page holds the crawl-relevant essentials and points at the source page (`source_url`) for full detail — we don't duplicate the entire source page into the page.

Modules: `mindfulness`, `distress-tolerance`, `emotion-regulation`, `interpersonal-effectiveness`.

## Node (page) frontmatter

```yaml
id: distress-tolerance/tipp        # stable slug, == path under pages/ w/o .md
title: TIPP
module: distress-tolerance
page_no: T10                       # label from the source site (e.g. T10)
source_url: https://dialecticalbehaviortherapy.com/distress-tolerance/tipp/
type: skill                        # skill | acronym-step | concept | decision-point
summary: >                         # 1–2 sentences, shown in previews
  Fast body-based skills to bring down extreme arousal in minutes.
tags: [crisis, high-arousal, physiological]
when_to_use: >
  Emotion is at crisis intensity (roughly 8–10/10) and you cannot think.
when_not_to_use: >
  Heart conditions (cold water / intense exercise cautions).
edges:                             # outgoing pointers, see below
  - to: distress-tolerance/stop
    relation: alternative_to
    note: STOP is the cognitive-brake sibling to TIPP's body-brake.
```

The body of the file (below the frontmatter) holds the full `practice` instructions in prose — the part a client renders when you land on the page.

### Authoring guardrail: 3–6 outbound edges per page

Aim for **3 to 6 outgoing edges** on each page. This is a signal, not a hard limit:

- **Fewer than 3** usually means the page is *orphaned* — we're missing pointers, or it isn't well connected into the web.
- **More than 6** usually means the page *isn't atomic* — it's doing too much and should probably be split into smaller pages.

Entry ramps and hub pages are allowed to exceed this deliberately.

## Edge (pointer) fields

| field       | meaning                                                        |
|-------------|----------------------------------------------------------------|
| `to`        | target page id                                                 |
| `relation`  | typed semantics of the pointer (see vocabulary below)          |
| `condition` | optional guard, natural language, e.g. "if urge to act on it"  |
| `note`      | **required** — why this pointer exists (for editing + for the crawler's why) |

`note` is mandatory on every edge. Best practice from typed-link systems: briefly say *why* two pages connect, and pick the relation that is *most true*, not the most generic. This is what stops every pointer from collapsing into `pairs_with`.

### Relation vocabulary

| relation          | traversal meaning                                                    |
|-------------------|----------------------------------------------------------------------|
| `escalates_to`    | when this isn't enough, go here (more intensive)                     |
| `de_escalates_to` | the calmer / next-step move after this one                           |
| `prerequisite_of` | you generally need the target skill first                            |
| `builds_on`       | the target is foundational; this page extends or applies it (reverse of `prerequisite_of`) |
| `part_of`         | this page is a component of the target (e.g. a letter of an acronym) |
| `alternative_to`  | a sibling skill for the same situation                               |
| `contrasts_with`  | deliberately different approach; compare / choose                    |
| `pairs_with`      | commonly used together                                               |
| `if_condition`    | conditional branch; requires `condition`                            |

## Entry ramps (`ramps.yaml`)

Not a single start node. Several ways you actually arrive at the web:

- **felt state** — "panicking", "numb", "resentful"
- **situation** — "conflict with a person", "urge to act on impulse"
- **goal** — "I want to ask for something", "I want to tolerate this moment"

Each ramp lists edges into the relevant pages. See `ramps.yaml`.

## Backlinks (reverse index)

Edges are stored *on the originating page* so authoring stays local — when you edit a page you see its outgoing pointers. The cost is that "what points *at* TIPP?" would require scanning every file.

We resolve this with a **build step** — `python build.py` (no dependencies) — run whenever pages change. It reads all pages and emits a derived `backlinks.json` mapping each page id to its incoming edges. Authors never hand-maintain it. The crawler and any future client can then traverse in both directions cheaply. Pages remain the single source of truth; the reverse index is generated, never edited.

`build.py` also validates the graph and exits non-zero on a real error: it reports unresolved edge targets (splitting expected cross-module edges from broken intra-module ones), flags any page outside the 3–6 edge guardrail, and checks that every `ramps.yaml` target resolves to a real page.

## How the crawler uses this

1. Match the user's opening to a ramp.
2. Follow edges, prioritizing by relation type for the scenario (a crisis prioritizes `if_condition` / `de_escalates_to`; a planning scenario prioritizes `prerequisite_of` / `pairs_with`).
3. Evaluate `condition` guards against what the user reports.
4. Land on a page, surface its `practice`, and offer the next pointers.

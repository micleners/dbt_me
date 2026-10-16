---
type: proposal
status: open
created: 2026-10-12
updated: 2026-10-13
linked_from: system_enhancement.md §6
depends_on: investigations/mindfulness-what-how-skills.md
---

# Deck integration proposal

## Model

- Treat the deck like the site: `supplemental_dbt_flashcards/` is the deck's source layer, as `raw/` is the site's.
- Never edit a site-sourced page's body with deck content. Keep provenance separable.
- Give each deck card exactly one integration action:

| Action | Use when | Result |
|---|---|---|
| `supplement` | A graph page already teaches the skill; the deck adds practices or angles. | Deck file links to that page. Clients offer it as extra practice. |
| `new-node` | The deck teaches a skill the graph lacks, and a ramp could plausibly land on it. | New graph page authored from the deck file. |
| `hub` | Overview deck card grouping other skills. | New `type: concept` page; members point to it with `part_of`. |
| `defer` | The matching page is in an unbuilt module. | Record target now; resolve when the module is built. |

- Choose `new-node` only for a distinct skill. A new practice variant of an existing skill is a `supplement`.

## Proposed dispositions (deck 001–015)

| Deck card | Action | Target |
|---|---|---|
| 001 The What Skills | hub | `mindfulness/what-skills` (new) |
| 002 Observe | supplement | `mindfulness/observing` |
| 003 Describe | supplement | `mindfulness/mental-noting` |
| 004 Participate | new-node | `mindfulness/participate` (new) |
| 005 The How Skills | hub | `mindfulness/how-skills` (new) |
| 006 Nonjudgmentally | supplement | `mindfulness/mindfulness-of-negative-judgments` |
| 007 One-mindfully | supplement | `mindfulness/observing` |
| 008 Effectively | defer | `emotion-regulation/being-effective` (E2, uncarded) |
| 009 Wise Mind | supplement | `mindfulness/wise-mind` |
| 010 Wise Mind Practices | supplement | `mindfulness/wise-mind` |
| 011 Skillful Means | new-node | `mindfulness/skillful-means` (new) |
| 012 Observing the Breath | supplement | `mindfulness/mindful-breathing` |
| 013 Do a Body Scan | supplement | `mindfulness/mental-body-scan` |
| 014 External Mindfulness Ideas | supplement | `distress-tolerance/grounding` |
| 015 Loving-Kindness | new-node | `mindfulness/loving-kindness` (new) |

Totals: 9 supplement, 3 new-node, 2 hub, 1 defer.

## Mechanism

1. Add an `integration` block to each deck file's frontmatter. The link lives only on the deck side:
   ```yaml
   integration:
     action: supplement        # supplement | new-node | hub | defer
     target: mindfulness/observing
   ```
2. Extend `build.py`:
   - Validate `supplement` targets resolve to real pages. Allow `defer` targets in unbuilt modules.
   - Generate `supplements.json`: graph page id → list of deck file paths. Never hand-edited.
   - Deck files stay out of the node set and the 3–6 edge guardrail.
3. Extend `SCHEMA.md` for deck-sourced nodes:
   - `source_url` optional when `source: deck` and `deck_card_no` are set.
   - Continue module numbering (M11, M12, ...).
   - The deck file is the source record, as a `raw/` page is for site pages.
4. Add a `dbt-conversation` rule: when delivering a page, offer its supplements as optional extra practices.
5. Add the `integration` block to the `dbt-flashcard-ingest` skill's frontmatter template and steps.

## Open decisions

- **Investigation outcome** changes 001, 004, 005:
  - Site overview teaches What/How → hubs are site-sourced; 001 and 005 become `supplement`.
  - Site has a Participate page → Participate is site-sourced; 004 becomes `supplement`.
  - Site lacks them → deck must source those pages; resolve `system_enhancement.md` §5.
- **Hub guardrail:** hubs get mostly incoming `part_of` edges. Either exempt `type: concept` from the 3–6 rule (recommended) or give hubs outgoing edges (e.g. what-skills `pairs_with` how-skills).
- **003 Describe and 007 One-mindfully:** `supplement` as proposed, or `new-node` under the hubs to mirror Linehan's What/How structure.

## Sequence

1. Run the investigation.
2. Add `integration` to the ingest skill; backfill all deck files.
3. Extend `build.py` (validation + `supplements.json`).
4. Update `SCHEMA.md` (deck-sourced nodes, hub guardrail).
5. Author new nodes and hubs; add ramps.
6. Add the supplement rule to `dbt-conversation`.

Steps 2–3 do not depend on the investigation.

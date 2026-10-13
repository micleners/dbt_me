---
name: dbt-flashcard-ingest
description: Logs a card from the physical DBT flash card deck into supplemental_dbt_flashcards/. Use when given photos of a deck card (front and/or back) or asked to add, document, or log a flashcard.
---

# Ingest a DBT deck flashcard

Deck cards sit outside the graph: `build.py` reads only `pages/`, and `ramps.yaml` never points here.

## Steps

1. Read the front (number, title, tagline, module label) and back (body, practice suggestions). If a side is missing or unreadable, ask for it.
2. Assess overlap: decide which existing skills already teach this card's content. Check graph pages in `pages/` first, then unbuilt modules' raw pages in `raw/emotion-regulation/` and `raw/interpersonal-effectiveness/`. Set `coverage` to `strong` (an existing page teaches the same practice), `partial` (related, but the card adds a technique or angle), or `none`.
3. Write the file in the format below, following the "Writing page content" rules in `CLAUDE.md`.
4. Run `python build.py`; it must still pass.
5. Report the overlap verdict and the gap in 1–2 sentences.
6. Commit and push.

## Path

`supplemental_dbt_flashcards/<module>/<###>-<card-title>.md`

- `<module>`: `mindfulness`, `distress-tolerance`, `emotion-regulation`, or `interpersonal-effectiveness`. A deck label outside these four gets its own kebab-case folder.
- `<###>`: printed deck number, zero-padded. Not a repo `page_no`.
- `<card-title>`: printed title, kebab-case.

## Frontmatter

```yaml
deck_card_no: 15                    # printed number
title: Loving-Kindness              # printed title, as-is
tagline: Bring compassion into mindfulness.  # front subtitle, paraphrased
deck_module: MINDFULNESS            # printed module label, as-is
module: mindfulness                 # repo module slug
deck: TBD                           # deck title/publisher
references_deck_cards: []           # deck numbers the text cites ("Card 2" -> 2)
repo_overlap:
  coverage: none                    # none | partial | strong
  related: []                       # overlapping page ids or raw/ paths
  gap: ...                          # what the card adds that the repo lacks
```

## Body

- `## Summary`: paraphrase of what the skill is and why it helps.
- `## Practice`: paraphrase of the practice suggestions, same steps and order.
- `## Notes`: our overlap reasoning and integration ideas.

Example: `supplemental_dbt_flashcards/mindfulness/015-loving-kindness.md`.

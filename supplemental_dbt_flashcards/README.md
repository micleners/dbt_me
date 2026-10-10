# Supplemental DBT flashcards

A holding area for transcriptions of a physical DBT flash card deck, documented card by card. This content is **not** part of the graph: `build.py` only reads `cards/`, and nothing here is linked from `ramps.yaml`. How (or whether) each card gets folded into the graph is decided later; the `repo_overlap` block on each card records the starting assessment.

## Layout

```
supplemental_dbt_flashcards/<module>/<###>_<card_title>.md
```

- `<module>` uses the repo's module slugs: `mindfulness`, `distress-tolerance`, `emotion-regulation`, `interpersonal-effectiveness`. A deck category that isn't one of the four gets its own folder named after the label printed on the card.
- `<###>` is the deck's printed card number, zero-padded to three digits. It is the deck's number, not a repo `card_no` (M1, T5, ...).
- `<card_title>` is the printed title in lowercase snake_case.

## Card format

Frontmatter:

| Field | Meaning |
|---|---|
| `deck_card_no` | Number printed on the card (integer). |
| `title` | Title printed on the front, verbatim. |
| `tagline` | One-line subtitle printed on the front, verbatim. |
| `deck_module` | Module label printed on the front, verbatim. |
| `module` | Repo module slug that label maps to. |
| `deck` | Which deck this came from (title/publisher), once known. |
| `references_deck_cards` | Other deck card numbers the text cites, e.g. "Observing (Card 2)". |
| `repo_overlap.coverage` | `none`, `partial`, or `strong`: how much of this card the graph already captures. |
| `repo_overlap.related` | Existing repo card ids (or `raw/` pages) that overlap. |
| `repo_overlap.gap` | What the card adds that the repo lacks. |

Body:

- `## Front` and `## Back` hold the deck's text **verbatim**: wording, headings and lists kept as printed. Words hyphenated across a printed line break are rejoined, and paragraphs are single lines (no hard wrapping).
- `## Notes` holds anything that is ours rather than the deck's (overlap reasoning, integration ideas). Keep the deck's text and our commentary separate so the verbatim part stays clean.

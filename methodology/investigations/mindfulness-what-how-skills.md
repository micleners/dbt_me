# Investigation: are the "What" and "How" skills on the source site?

Status: **open**. Linked from `methodology/system_enhancement.md` §5.

## Question

- Does https://dialecticalbehaviortherapy.com teach Linehan's core mindfulness skills anywhere?
  - "What" skills: Observe, Describe, Participate.
  - "How" skills: Nonjudgmentally, One-mindfully, Effectively.
- Did the Mindfulness fetch (M1–M10) miss them, or does the site simply not cover them?

## Known so far

- The flash card deck covers all six (`supplemental_dbt_flashcards/mindfulness/001`–`008`). Participate has no graph card at all.
- The cached pages' previous/next links chain M1 → M10 with no gaps, and M10 has no "next". The exercise list is complete at 10, and none of them is Participate.
- "Participate", "What skills" and "How skills" appear in no file under `raw/mindfulness/`.
- **Never cached:** the Mindfulness overview page. M1 links back to it as `https://dialecticalbehaviortherapy.com/?page_id=8` (probably `/mindfulness/`). This is the most likely place for the What/How skills.
- The first attempt failed because the cloud environment's network policy blocks `dialecticalbehaviortherapy.com`. Run this from a session that can reach it.

## Steps

1. Fetch the overview page: try `https://dialecticalbehaviortherapy.com/mindfulness/`, then `https://dialecticalbehaviortherapy.com/?page_id=8`. Get raw HTML with `curl` and convert to text; the WebFetch summarizer truncates lists (see `module_fetch.md` step 1).
2. Search the page text for: participate, observe, describe, nonjudgmental, one-mindful, effective, "what skills", "how skills".
3. Check the site's search and sitemap (`/sitemap.xml`, `/wp-sitemap.xml`, `/?s=participate`) for a standalone Participate or What/How page in any module path.
4. Record the result below.

## Outcomes

- **Overview teaches What/How:** cache it as `raw/mindfulness/M00-overview.md` (with `source_url` + `fetched` frontmatter). Then decide whether it becomes a hub card or `## Notes` material on M1. A hub card needs a new `card_no` scheme, so log that decision in `system_enhancement.md`.
- **Separate Participate (or What/How) page exists:** this is a missed fetch. Cache it, build the card, and update the M-count in `CLAUDE.md` and `module_fetch.md`.
- **Site doesn't cover them:** close this file as "not on source site". Graph cards for Participate and the How skills then need a source other than the site. Decide in `system_enhancement.md` §5 whether the deck can be that source.

## Result

_Not yet run._

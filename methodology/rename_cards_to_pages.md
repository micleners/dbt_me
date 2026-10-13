# Handoff: rename graph "cards" to "pages"

Rename the graph's nodes from "card" to "page" so "card" means only a physical flash card from the deck. Work forward on `main`; do not rewrite history.

## Sections

- Terminology
- Rules
- Steps
- Per-file edits
- Verification
- Commit

## Terminology

| Old | New | Meaning |
|---|---|---|
| card (graph node) | page | One node in `pages/<module>/`, distilled from one webpage. |
| `cards/` | `pages/` | Directory of graph nodes. |
| `card_no` | `page_no` | Frontmatter field (T1, M4, ...). |
| raw page / page dump | raw page | Fetch cache in `raw/`. Unchanged. |
| webpage on the source site | source page | Use "source page" wherever "page" alone would be ambiguous. |
| deck card, flash card, flashcard | unchanged | Physical deck. |
| diary card | unchanged | External DBT term in `validation/`. |

## Rules

- Rename only words that mean a graph node. Leave every deck, flashcard, and diary-card usage alone.
- Card ids (`mindfulness/describe-your-emotions`) contain no "card"; they do not change. `backlinks.json` ids and `ramps.yaml` targets stay valid.
- Use `git mv` for the directory so git tracks the files as renamed, not deleted and re-added.
- Edit file by file with the list below. Do not run a repo-wide `sed s/card/page/`.
- Fix grammar after each swap ("a page", "pages hold").
- When "page" would collide with a source webpage or raw page, write "source page" or "raw page".
- Follow `CLAUDE.md` style rules: no em-dashes as punctuation; run `wc -lc` before and after editing `CLAUDE.md` and each `SKILL.md`; neither may grow.

## Steps

1. `git mv cards pages`.
2. In every `pages/**/*.md`, rename the frontmatter key `card_no:` to `page_no:` (exactly 23 files; this one `sed` is safe because the key is unique): `sed -i '' 's/^card_no:/page_no:/' pages/*/*.md`.
3. Edit `build.py` (see below), then run `python build.py`. It must report 23 pages parsed and the same edge counts as before (83 edges total: 49 + 34) with no new errors.
4. Edit the docs and skills in the per-file list.
5. Run the verification greps.
6. Commit and push.

## Per-file edits

**`build.py`**
- `CARDS_DIR = ROOT / "cards"` → `PAGES_DIR = ROOT / "pages"`; update every use.
- `parse_card` → `parse_page`; local vars `card`/`cards`/`cid` → `page`/`pages`/`pid`.
- Regex `(id|title|card_no)` → `(id|title|page_no)`; dict key and `.get('card_no','?')` → `page_no`.
- Docstrings and print strings: "Cards parsed" → "Pages parsed", "3-6 per card" → "3-6 per page", "all cards within 3-6" → "all pages within 3-6", "real cards" → "real pages".

**`SCHEMA.md`** (about 22 hits, all graph nodes)
- "Cards are nodes" → "Pages are nodes"; "Node (card) frontmatter" → "Node (page) frontmatter".
- Tree: `cards/` → `pages/`; `<module>/<card>.md` → `<module>/<page>.md`; in the `raw/` line, `T##-<card>.md` → `T##-<page>.md`.
- Line 20: "Cards are distilled from `raw/`... we don't duplicate the entire page into the card" → "Pages are distilled from `raw/`... we don't duplicate the entire source page into the page".
- `id` comment: "path under cards/" → "path under pages/". Line 30: `card_no: T10  # label from the source deck/site` → `page_no: T10  # label from the source site` (drop "deck"; it collides with the flash card deck).
- Guardrail section, edge table, relation table, build section: card → page throughout ("hub pages", "target page id", "source page" for where edges are stored: reword to "the originating page" to avoid the source-site meaning).

**`CLAUDE.md`**
- Line 3: "skill cards" → "skill pages".
- Line 5: "Cards paraphrase ...: one page = one card = one node" → "Pages paraphrase ...: one source page = one page = one node".
- Structure block: "Data model: cards, ..." → "pages"; `cards/<module>/  One Markdown+YAML card per page` → `pages/<module>/  One Markdown+YAML page per source page`. Keep line 16 and line 18 (deck cards).
- Status: "13 cards", "10 cards", "cards not built" → pages. Keep "one file per card as photos arrive" (deck).
- "## Writing card content" → "## Writing page content"; "Applies to `cards/`" → "`pages/`".
- Keep line 41 (deck cards). Line 45: "cards hold *which skill and why*" → "pages hold".
- Workflow: "any card or ramp change", "a card outside 3–6 edges" → page.

**`README.md`**
- Lines 3, 5, 24, 36, 40: graph cards → pages; `cards/<module>/` → `pages/<module>/`. Line 3 also has an em-dash pair; replace with commas while editing.

**`ramps.yaml`**
- Comments on lines 3 and 6: "cards' own typed edges" → "pages' own typed edges"; "a card id" → "a page id".

**`.claude/skills/dbt-conversation/SKILL.md`**
- "card body" → "page body"; "a card" (line 8) → "a page"; "best-matching cards", "edges in `cards/`" → pages, `pages/`.

**`.claude/skills/dbt-flashcard-ingest/SKILL.md`**
- Keep name, description, title, and every deck-card use (lines 2, 3, 6, 21, 25, 36, 40, 49).
- Line 8: "Supplemental cards sit outside the graph: `build.py` reads only `cards/`" → "Deck cards sit outside the graph: `build.py` reads only `pages/`".
- Line 13: "Check graph cards in `cards/` first, then uncarded modules' pages in `raw/`" → "Check graph pages in `pages/` first, then unbuilt modules' raw pages in `raw/`".
- Line 14: `"Writing card content"` → `"Writing page content"` (must match the renamed `CLAUDE.md` heading).
- Line 39: "overlapping card ids" → "overlapping page ids".

**`methodology/module_fetch.md`**
- Status lines 7–10: "13 cards", "10 cards", "12 cards", "13 cards" → pages.
- Step 1 "Enumerate the deck" → "Enumerate the module's pages" (here "deck" means site pages; it collides with the flash card deck).
- Step 2 "Card URLs" → "Source page URLs". Step 3 and line 44: "one page = one card = one node" → "one source page = one page = one node".
- Step 5: "Author cards", `cards/<module>/<slug>.md`, `card_no` → "Author pages", `pages/<module>/<slug>.md`, `page_no`.
- Lines 43, 46, 49: card → page.

**`methodology/deck_integration.md`**
- Graph-node uses → page: "site-sourced card's body" → "site-sourced page's body"; table cells "A graph card already teaches", "links to that card", "New graph card", "New `type: concept` card", "The matching card"; "real cards"; "graph card id"; "for site cards"; "delivering a card"; "deck must source those cards" → pages.
- Keep "deck card" everywhere (line 9, the "Deck card" column header, etc.).

**`methodology/system_enhancement.md`**
- Line 13 "foundation cards", line 25 "card + edge `note`", line 39 "no graph cards", line 47 "supplement an existing card", line 51 "per-card dispositions" → page. Keep "deck card(s)" on lines 47 and 49 and "flash card deck" on line 39.

**`methodology/investigations/mindfulness-what-how-skills.md`**
- Line 14 "no graph card" → "no graph page"; line 30 "build the card" → "build the page"; line 31 "Graph cards" → "Graph pages". Keep "flash card deck".

**`validation/research-summary.md`**
- Line 5 "skill cards" and line 17 "per card", "the card is orphaned / not atomic" → page. Keep every "diary card".

**Leave untouched**
- `supplemental_dbt_flashcards/**` (all hits are deck cards).
- `raw/**`, `backlinks.json` (regenerated by `build.py`; ids unchanged).
- This handoff file: delete it in the final commit once the rename lands.

## Verification

- `python build.py` exits 0, prints "Pages parsed: 23", and `git diff backlinks.json` is empty.
- `test ! -e cards && ls pages` shows both modules.
- `grep -rnIiE '\bcards?\b|card_no|CARDS_DIR|parse_card' --exclude-dir=.git --exclude-dir=supplemental_dbt_flashcards --exclude-dir=raw .` returns only deck, flashcard, and diary-card lines. Read each remaining hit and justify it.
- `grep -rn 'Writing page content' CLAUDE.md .claude` shows the heading and the skill's reference.
- `wc -lc CLAUDE.md .claude/skills/*/SKILL.md`: no file grew.
- `git status` shows `cards/... -> pages/...` as renames.

## Commit

- One commit: `Rename graph cards to pages`, body noting the `card_no` → `page_no` field rename. Delete this handoff file in the same commit.
- End the message with the `Co-Authored-By` line from the session's attribution reminder.
- Push to `origin main`.

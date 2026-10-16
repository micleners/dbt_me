---
type: plan
status: open
created: 2026-10-16
updated: 2026-10-16
linked_from: system_enhancement.md §7
blocks: cross-module linking pass
---

# Edge cap vs. cross-module links

## Problem

- `SCHEMA.md` asks for 3–6 outbound edges per page; `build.py` enforces it.
- Modules were built in order (Distress Tolerance, Mindfulness, Interpersonal Effectiveness, Emotion Regulation), and each could only link to modules that already existed.
- Result: Mindfulness links to no other module; Distress Tolerance links only to Mindfulness (5 edges). Nothing links forward into a later module.
- Most pages already sit at 3–6 same-module edges, so adding cross-module links breaks the cap.

## Possible solutions

1. **Raise the cap** (e.g. 3–8). Simplest; weakens the "more than 6 means not atomic" signal.
2. **Count only same-module edges** toward 3–6; give cross-module edges their own cap (e.g. 0–3). Keeps the atomicity signal per module.
3. **Swap, don't add.** Keep 3–6 total; a cross-module link replaces the weakest same-module edge. Forces ranking; may drop true edges.
4. **Keep cross-module links out of pages.** Store them in a separate file (e.g. `bridges.yaml`) that `build.py` merges. Pages stay untouched; the graph gets a second home for edges.

## Open questions

- Should the cap stay a warning or an error?
- Does a cross-module edge need a stricter bar (e.g. only `prerequisite_of`, `builds_on`, `contrasts_with`)?

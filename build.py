#!/usr/bin/env python3
"""Build step for the DBT skills web.

Reads every card under cards/, validates the edge graph, and generates
backlinks.json (the reverse index). No external dependencies.

Validation performed:
  - unresolved edge targets (split into cross-module = expected future work,
    vs intra-module = a real broken link)
  - the 3-6 outbound-edges authoring guardrail
  - ramp targets in ramps.yaml resolve to real cards

Run: python build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CARDS_DIR = ROOT / "cards"
RAMPS_FILE = ROOT / "ramps.yaml"
OUT_FILE = ROOT / "backlinks.json"

# Modules we have not built yet — edges into them are expected, not errors.
FUTURE_MODULES = {"emotion-regulation", "interpersonal-effectiveness"}


def split_frontmatter(text):
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def parse_card(path):
    """Extract id, title, card_no, and outgoing edges from a card file."""
    fm = split_frontmatter(path.read_text(encoding="utf-8"))
    card = {"id": None, "title": None, "card_no": None, "edges": []}
    in_edges = False
    edge = None
    for line in fm.splitlines():
        # top-level scalar keys (no indentation)
        m = re.match(r"^(id|title|card_no):\s*(.+)$", line)
        if m and not in_edges:
            card[m.group(1)] = m.group(2).strip()
            continue
        if re.match(r"^edges:\s*$", line):
            in_edges = True
            continue
        if not in_edges:
            continue
        # new edge item: "  - to: <id>"
        m = re.match(r"^\s*-\s*to:\s*(.+)$", line)
        if m:
            if edge:
                card["edges"].append(edge)
            edge = {"to": m.group(1).strip()}
            continue
        # edge fields: "    relation: ..." / "    note: ..." / "    condition: ..."
        m = re.match(r"^\s+(relation|note|condition):\s*(.+)$", line)
        if m and edge is not None:
            edge[m.group(1)] = m.group(2).strip()
    if edge:
        card["edges"].append(edge)
    return card


def parse_ramp_targets(path):
    """Lightweight pull of every `to:` under ramps.yaml (indented deeper than cards)."""
    if not path.exists():
        return []
    targets = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s+-?\s*to:\s*(.+)$", line)
        if m:
            targets.append(m.group(1).strip())
    return targets


def module_of(card_id):
    return card_id.split("/", 1)[0] if "/" in card_id else ""


def main():
    cards = {}
    for path in sorted(CARDS_DIR.rglob("*.md")):
        card = parse_card(path)
        if not card["id"]:
            print(f"WARN: {path} has no id, skipping")
            continue
        cards[card["id"]] = card

    ids = set(cards)
    # Sorted keys and entries keep backlinks.json byte-stable across runs.
    backlinks = {cid: [] for cid in sorted(ids)}
    unresolved_cross, unresolved_broken = [], []

    for cid, card in cards.items():
        for e in card["edges"]:
            tgt = e["to"]
            if tgt in ids:
                backlinks[tgt].append(
                    {"from": cid, "relation": e.get("relation"), "note": e.get("note")}
                )
            elif module_of(tgt) in FUTURE_MODULES:
                unresolved_cross.append((cid, tgt))
            else:
                unresolved_broken.append((cid, tgt))

    for entries in backlinks.values():
        entries.sort(key=lambda b: (b["from"], b["relation"] or ""))
    OUT_FILE.write_text(json.dumps(backlinks, indent=2), encoding="utf-8")

    # ---- report ----
    print(f"Cards parsed:        {len(cards)}")
    total_edges = sum(len(c['edges']) for c in cards.values())
    print(f"Outgoing edges:      {total_edges}")
    print(f"Backlinks written:   {OUT_FILE.name}\n")

    print("Edge-count guardrail (3-6 per card):")
    off = False
    for cid, card in sorted(cards.items()):
        n = len(card["edges"])
        if n < 3 or n > 6:
            off = True
            print(f"  ! {card.get('card_no','?'):>3} {cid}: {n} edges")
    if not off:
        print("  all cards within 3-6")

    print("\nCross-module edges (expected future work):")
    if unresolved_cross:
        for src, tgt in unresolved_cross:
            print(f"  ~ {src} -> {tgt}")
    else:
        print("  none")

    print("\nBROKEN intra-module edges (must fix):")
    if unresolved_broken:
        for src, tgt in unresolved_broken:
            print(f"  X {src} -> {tgt}")
    else:
        print("  none")

    print("\nRamp targets:")
    ramp_targets = parse_ramp_targets(RAMPS_FILE)
    bad = [t for t in ramp_targets if t not in ids]
    print(f"  {len(ramp_targets)} targets, {len(bad)} unresolved")
    for t in bad:
        print(f"  X ramp -> {t}")

    # non-zero exit if a real error exists
    if unresolved_broken or bad:
        sys.exit(1)


if __name__ == "__main__":
    main()

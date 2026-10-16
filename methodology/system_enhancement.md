---
type: backlog
status: active
created: 2026-09-02
updated: 2026-10-16
scope: Cross-cutting decisions about the data model, graph, and clients.
---

# System enhancements

High-level strategies and structural improvements surfaced during the work, parked here to act on deliberately later rather than mid-task. Each is a decision or change to the *system* (the data model, the graph, the client architecture) — not a step in building any one module (that was `archive/module_fetch.md`).

Status legend: **open** (not started) · **planned** (has a trigger) · **done**.

## 1. Add a `builds_on` relation — done

**What:** Add `builds_on` to the relation vocabulary in `SCHEMA.md` as the reverse of `prerequisite_of`, so a skill can point back at the foundation it depends on.

**Why:** Building Distress Tolerance exposed a gap — there is no way to say "Grounding *builds on* Observing" from Grounding's side. The only workaround was `pairs_with`, which understates a real dependency. Distress Tolerance already has 5 dangling cross-module edges into Mindfulness that want this direction.

**Done:** in `SCHEMA.md`; used across modules.

## 2. Watch for missing ramp categories — open

**What:** Expand `ramps.yaml` as felt states surface that no ramp cleanly matches.

**Why:** A real crawl ("lonely, insecure, rejected after a friend didn't answer") had no clean entry ramp — the closest was a goal ramp, which routed acceptably but not precisely. Loneliness / rejection / social hurt is a common enough entry state to deserve its own ramp.

**Trigger:** Ongoing. Every smoke-test crawl that lands on a poor ramp match is a candidate to log here and add.

## 3. Decide the data-vs-delivery contract — open

**What:** Decide how much of the client's *delivery* is deterministic (rendered straight from page + edge `note`) vs. generated per-person (an LLM writing situation-specific, empathic wording on top of the graph).

**Why:** In a live crawl the graph supplied the skills (Self-Soothing, ACCEPTS→Contributing, RESISTT→Reframe) but the empathic sentence tying them to the person's exact situation was generated on top, not stored in a page. That seam is the core architecture question for the eventual web app: a "dumb" client shows the page; a "smart" client generates the delivery. The graph must stay the source of truth for *which skill and why*; clients must not invent skills the graph doesn't contain.

**Trigger:** When starting the web app / client work.

## 4. Modeling note: the distraction-vs-acceptance axis — reference

**What:** Not a change — a convention to reuse. The recurring tension between *distract away from* a feeling and *stay with / accept* it is well captured by `contrasts_with` (e.g. ACCEPTS / RESISTT vs. Urge Surfing).

**Why:** Recording it so future modules model the same axis consistently instead of inventing new relations for it.

## 5. Mindfulness "What"/"How" skills missing from the graph — open

**What:** Participate and the three "How" skills (Nonjudgmentally, One-mindfully, Effectively) have no graph pages, though the flash card deck covers them.

**Why:** It's unclear whether the source site lacks them or the M1–M10 fetch missed its overview page. If the site lacks them, decide whether a non-site source (the deck) may back a graph page.

**Trigger:** Next session with network access to the source site. Procedure and findings: `methodology/investigations/mindfulness-what-how-skills.md`.

## 6. Integrate deck flashcards into the graph — open

**What:** Give each deck card one action (supplement an existing page, new node, hub, or defer) and wire supplements in via a generated `supplements.json`.

**Why:** Deck cards 001–015 overlap the Mindfulness graph unevenly: most add practices to existing pages, three teach skills the graph lacks.

**Trigger:** After the What/How investigation (§5). Proposal and per-card dispositions: `methodology/deck_integration.md`.

## 7. Edge cap vs. cross-module links — open

**What:** Decide how the 3–6 outbound-edge guardrail treats cross-module links.

**Why:** Modules built early have no links to later ones; adding them pushes pages past 6.

**Trigger:** Before the cross-module linking pass. Plan: `methodology/edge_cap.md`.

## 8. Scenario run-throughs — open

**What:** Use example scenarios to find dead ends and missing links in the graph.

**Why:** The two smoke tests at build time each found a fix; there is no repeatable version.

**Trigger:** After §7. Plan: `methodology/scenario_testing.md`.

# System enhancements

High-level strategies and structural improvements surfaced during the work, parked here to act on deliberately later rather than mid-task. Each is a decision or change to the *system* (the data model, the graph, the client architecture) — not a step in building any one module (that's `module_fetch.md`).

Status legend: **open** (not started) · **planned** (has a trigger) · **done**.

## 1. Add a `builds_on` relation — planned

**What:** Add `builds_on` to the relation vocabulary in `SCHEMA.md` as the reverse of `prerequisite_of`, so a skill can point back at the foundation it depends on.

**Why:** Building Distress Tolerance exposed a gap — there is no way to say "Grounding *builds on* Observing" from Grounding's side. The only workaround was `pairs_with`, which understates a real dependency. Distress Tolerance already has 5 dangling cross-module edges into Mindfulness that want this direction.

**Trigger:** Do it when building the **Mindfulness** module (those foundation cards — Observing, Wise Mind, Mindful Breathing — come into existence then, and the cross-module edges resolve at the same time).

## 2. Watch for missing ramp categories — open

**What:** Expand `ramps.yaml` as felt states surface that no ramp cleanly matches.

**Why:** A real crawl ("lonely, insecure, rejected after a friend didn't answer") had no clean entry ramp — the closest was a goal ramp, which routed acceptably but not precisely. Loneliness / rejection / social hurt is a common enough entry state to deserve its own ramp.

**Trigger:** Ongoing. Every smoke-test crawl that lands on a poor ramp match is a candidate to log here and add.

## 3. Decide the data-vs-delivery contract — open

**What:** Decide how much of the client's *delivery* is deterministic (rendered straight from card + edge `note`) vs. generated per-person (an LLM writing situation-specific, empathic wording on top of the graph).

**Why:** In a live crawl the graph supplied the skills (Self-Soothing, ACCEPTS→Contributing, RESISTT→Reframe) but the empathic sentence tying them to the person's exact situation was generated on top, not stored in a card. That seam is the core architecture question for the eventual web app: a "dumb" client shows the card; a "smart" client generates the delivery. The graph must stay the source of truth for *which skill and why*; clients must not invent skills the graph doesn't contain.

**Trigger:** When starting the web app / client work.

## 4. Modeling note: the distraction-vs-acceptance axis — reference

**What:** Not a change — a convention to reuse. The recurring tension between *distract away from* a feeling and *stay with / accept* it is well captured by `contrasts_with` (e.g. ACCEPTS / RESISTT vs. Urge Surfing).

**Why:** Recording it so future modules model the same axis consistently instead of inventing new relations for it.

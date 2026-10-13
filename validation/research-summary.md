# Schema Validation — Research Summary

Date: 2026-09-02

External research to pressure-test the `SCHEMA.md` data model (typed-edge graph of DBT skill pages, crawled from an entry ramp toward a suggestion). Verdict: the structure holds up; the research produced three additive guardrails, not a redesign.

## Verdict

1. **Typed-edge graph is the right backbone.** Knowledge-graph literature is consistent that relationships should be first-class, typed, stored objects with their own traversal semantics — "the schema lives in the edges themselves." This is exactly the bet made by the `relation` vocabulary in `SCHEMA.md`.

2. **Graph beats decision-tree for this use case.** Clinical-pathway / triage research reports that flowcharts and decision-trees are routinely *converted into directional graphs* because a tree "doubles back several times," whereas a graph yields the "shortest distance / fewer evaluations" from problem to recommendation. This supports building a navigable web rather than a fixed questionnaire.

3. **The concept fills a real market gap.** Every shipping DBT app is built around the *diary card* (tracker + reference manual + 0–7 skill checklist). None model the skills as a navigable web traversed from a felt state to a suggestion. There is no existing data model to copy — which validates designing our own.

## Refinements adopted from the research

1. **"3–6 outbound edges per page" authoring guardrail.** Typed-link (Zettelkasten) practitioners converged on this: fewer than 3 = the page is orphaned; more than 6 = the page is not atomic. Use as a signal to split a page or to find missing pointers.

2. **Mandatory `note` ("why") on every edge.** Best practice is to briefly explain *why* two notes are linked, and to "pick the relationship that is most true, not the most generic." Guards against every edge collapsing into a generic relation.

3. **Plan for backlinks / reverse traversal.** Clinical-pathway graphs distinguish state / decision / action nodes and rely on two-way navigation; Zettelkasten stresses two-way linking. Keep edges stored on the page (local authoring) and add a build step that computes a reverse (backlink) index, rather than moving to a central `edges.yaml`.

## Sources

### Knowledge graphs / typed edges
- Knowledge Graph Definition 101: How Nodes and Edges Connect Data — https://solutionsreview.com/data-management/knowledge-graph-definition-101-how-nodes-and-edges-connect-data/
- What Is a Knowledge Graph? How They Reduce LLM Hallucinations — https://atlan.com/know/what-is-a-knowledge-graph/
- What is a Knowledge Graph? Definition, Benefits, Use Cases — https://www.atscale.com/glossary/knowledge-graph/

### Graph vs. decision-tree for clinical pathways / triage
- Guideline2Graph: Profile-Aware Multimodal Parsing for Executable Clinical Decision Graphs — https://arxiv.org/pdf/2604.02477
- Multi-agent Self-triage System with Medical Flowcharts — https://arxiv.org/pdf/2511.12439
- CPGPrompt: Translating Clinical Guidelines into LLM-Executable Decision Support — https://arxiv.org/pdf/2601.03475

### Existing DBT apps (market gap)
- DBT Diary Card & Skills Coach — https://mwm.ai/apps/dbt-diary-card-skills-coach/479013889
- Diary Cards — Configurable Behavioral Tracking (TheraCharts) — https://theracharts.com/diary-cards/
- DBT Coach (App Store) — https://apps.apple.com/us/app/dbt-coach/id1452264969

### Typed links / linking practice (Zettelkasten)
- Zettelkasten Method: 7 Steps to Clear, Connected Notes — https://affine.pro/blog/zettelkasten-method
- Having two different types of links (Zettelkasten Forum) — https://forum.zettelkasten.de/discussion/3317/having-two-different-types-of-links
- Link notes. But how? (Obsidian Forum) — https://forum.obsidian.md/t/link-notes-but-how/58831

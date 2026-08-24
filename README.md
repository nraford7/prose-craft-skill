# prose-craft

A sentence-level writing skill for Claude Code. Three disciplines fused into one model, plus an optional fourth. The unit of work is the sentence; the unifying principle: nothing on the page by default.

| Axis | Source | Job |
|------|--------|-----|
| **Floor** | Strunk, *The Elements of Style* | Correctness and economy. Cut what is dead. |
| **Filter** | AI writing tropes ([tropes.fyi](https://tropes.fyi)) | Kill machine-tells. Remove what is automatic. |
| **Ceiling** | Virginia Tufte, *Grammar as Style* (1971) | Construct varied, intentional sentences. Add what does real work. |
| **Figure** (optional) | Classical rhetoric | Named schemes (antithesis, chiasmus, controlled repetition) for a piece's two or three anchor moments. Savored registers only. |

## Files

| File | Role |
|------|------|
| `SKILL.md` | The full model: three passes (Ceiling, then Filter, then Floor), conflict resolution, register calibration, a worked example, and a mechanical pre-delivery sweep. |
| `constructions.md` | The Ceiling catalog: branching, appositives, absolutes, the three series forms, syntactic symbolism. Real sentences from professional writers. |
| `figures.md` | The Figure catalog: surprise and repetition families, with the Filter reconciliation that keeps them rationed. |

## Workflow

Editing: **Ceiling first** (build on purpose), **Filter second** (cut the tells the build introduced), **Floor last** (tighten word by word). Build first, tighten last: tightening kills music you haven't written yet. Generating: construct with the Ceiling, then run Filter and Floor as one tightening pass.

## Boundaries

This skill governs voiced prose: essays, memos, reports, briefings, narrative and argument passages. Conversion copy with CTAs belongs to a persuasion-focused editing skill; technical docs, runbooks, and error messages belong to a controlled-language skill (ASD-STE100 style). Document-level argument structure is a layer above; personal voice is a layer above that.

## Maintenance

- The `writing-tropes` skill is the canonical tell list; the Filter here is its condensation. On any mismatch the stricter reading wins. Mirror edits both ways.
- Narrative-Engine (separate repo) embeds a copy of this skill so its build subagent is self-contained. Re-sync that copy after every change here.
- Caps (em-dashes, tricolons) are ceilings: a house or personal style guide layered above this skill may lower any of them, and the lower cap wins.

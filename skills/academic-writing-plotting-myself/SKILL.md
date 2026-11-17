---
name: academic-writing-plotting-myself
description: "Create, revise, and audit academic prose, LaTeX, tables, captions, and scientific figures with evidence-grounded, concise, reviewer-readable workflows. Use for manuscript writing, result interpretation, numerical consistency checks, and publication figures; do not use for unrelated general writing or product graphics."
---

# Academic Writing & Scientific Figures

This skill distills recurring problems from recent academic-writing and figure-making conversations. It keeps only broadly reusable practices: establish evidence before drafting, make claims proportional to the data, revise surgically, and verify the rendered artifact.

## Route the task

- For prose, LaTeX, tables, captions, result interpretation, or manuscript consistency, read references/writing-workflow.md.
- For a scientific figure, read references/figure-workflow.md.
- For a recurring failure mode or a request that seems underspecified, read references/recurrence-audit.md.

## Shared operating rules

1. Establish the source of truth before writing or plotting. Record the data source, version, experiment setting, model or condition, sample or seed aggregation, metric, and rounding rule. Do not silently mix stale manuscript text, archived results, checkpoints, subsets, or incompatible aggregations.
2. Preserve the artifact boundary. For drafting or revising LaTeX manuscript content, including large rewrites, return complete, directly pasteable LaTeX in the reply and identify the replacement location; do not edit `.tex` files by default. A request to revise manuscript content does not itself authorize writing to the source file. Write back only when the user explicitly requests direct modification of the specified `.tex` file. Do not ask for confirmation merely to return pasteable text: that is a completed deliverable. Preserve confirmed notation and surrounding wording outside the requested scope.
3. Separate evidence from interpretation. State what the table or figure reports, select the most informative comparison, and explain the narrow conclusion supported by it. Do not add unsupported mechanisms, statistical claims, or broad capability claims.
4. Prefer surgical revisions. Fix the requested symbol, sentence, table cell, or visual element without rewriting unrelated material or adding prose solely to increase length.
5. Keep the output auditable. Every numerical claim should be traceable to a source. If sources disagree, expose the conflict and resolve the provenance before choosing a value.

## Completion check

Before returning, verify that claims match the evidence, notation is consistent, displayed differences follow the requested rounding, LaTeX is usable, figures use honest and stable encodings, and no label, legend, table row, or annotation is clipped.

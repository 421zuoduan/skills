# Recurring problems abstracted from recent records

## Scope and method

This audit abstracts recurring issues from recent Codex and DSH harness conversations about academic manuscripts and scientific figures. Project names, benchmark names, paths, symbols, and method-specific rules have been removed so the findings apply to ordinary paper writing and research plotting. A coarse keyword scan covered 646 relevant prompts; categories overlap and the counts are only evidence of recurrence, not independent measurements.

The rough counts were: figure or layout requests 118; sample or seed aggregation 49; terminology or notation 37; result source or latest value 34; concise or too-long writing 33; do-not-edit-source or pasteable LaTeX 28; precision, rounding, or percent escaping 17.

## Recurring questions

| Repeated question | General lesson |
|---|---|
| Which result is current, and what source, condition, and aggregation produced it? | Freeze provenance before writing or plotting; stale and current results must not be mixed. |
| Can the source remain unchanged while the assistant returns pasteable text or code? | Respect the artifact boundary and identify the exact replacement span. |
| Is this paragraph too long or too detailed? | Keep only the evidence needed for the claim and the implication needed for the reader. |
| What do these numbers show beyond the fact that one method is larger? | Explain the capability or behavior supported by the selected comparison. |
| Are the symbols, terms, units, and definitions consistent? | Reuse established notation and terminology; do not introduce synonyms that change scope or meaning. |
| Was the reported difference computed with the requested precision? | Round displayed operands first, then calculate the displayed difference; keep units and percent escaping consistent. |
| Is the figure readable and balanced in the paper? | Judge the rendered artifact, not only the plotting code; check typography, whitespace, alignment, legend placement, and clipping. |
| Does the new figure preserve the established template and data meaning? | Reuse visual encodings where comparisons continue, preserve the original script, and never change data to obtain a preferred appearance. |

## Recurrent writing modes

1. Manuscript-safe revision: read context, identify the replacement span, make a minimal change, and return usable source text.
2. Evidence audit: reconcile source data, tables, figures, captions, and prose before proposing edits.
3. Results interpretation: choose a small number of decisive comparisons and connect them to the capability tested.
4. Technical consistency review: compare equations, pseudocode, implementation, and prose for mismatched assumptions.
5. Citation and format review: audit references and venue requirements as separate verification tasks.

## Recurrent figure modes

1. Publication cleanup: simplify the figure without removing evidence.
2. Template matching: keep encodings and dimensions comparable across related figures.
3. Data replacement: update values only after confirming provenance and aggregation.
4. Visual QA: render, inspect, and verify exports before delivery.

## Repeated failure modes

- Using a stale source, incompatible aggregation, or old image while calling it current.
- Computing differences from hidden unrounded values when the paper reports rounded values.
- Repeating every model, metric, or condition instead of selecting the result that changes the interpretation.
- Replacing notation or rewriting a whole section when only a local correction was requested.
- Treating visual emphasis as permission to fabricate uncertainty, alter data, or hide an inconsistent axis.

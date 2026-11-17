# Academic writing and LaTeX workflow

## Before drafting

Read the current manuscript in context and locate the exact passage, table, equation, caption, or label under discussion. For numerical claims, read the current result table or run summary and record the dataset, model or condition, split, sample or seed aggregation, checkpoint, metric, and precision. For implementation-sensitive claims, inspect the source code or experiment protocol rather than inferring behavior from prose alone.

## Output contract

- For drafting, polishing, or revising LaTeX manuscript prose, equations, tables, or captions, including large rewrites, do not modify `.tex` files by default. Return complete, directly pasteable LaTeX in the reply and briefly identify the replacement location.
- A request to revise manuscript content does not itself authorize writing to its source file. Write back only when the user explicitly requests direct modification of the specified `.tex` file; preserve the requested edit scope and do not ask again for the same authorized edit.
- Do not ask for confirmation merely to use the default pasteable-text workflow. Delivering the requested replacement text completes that task; direct file modification is not an additional required step.
- When returning LaTeX, use the notation and delimiters already used by the manuscript. Inline mathematics in source should use the requested delimiter consistently, and a literal percent should be escaped as \%.
- Keep a paragraph readable as a paragraph. Avoid artificial line breaks inside a sentence, and keep data belonging to one table row together when the requested format permits it.
- Preserve established symbols, index roles, units, and terminology. Do not rename notation or introduce synonyms merely to make a sentence sound different.
- Separate explanatory discussion from the final pasteable text.

## Paragraph logic

For a results paragraph, use this order: identify the table or figure and comparison; report one or two decisive patterns; explain what those patterns establish for the stated setting. Do not list every value, repeat an average after already giving the decisive contrast, or end with a generic claim that the method is effective. For a method or setting description, explain what capability is being evaluated before adding construction details. Keep detailed filtering, exclusions, and preprocessing in the appropriate methods or appendix section.

## Numerical checks

- Apply the requested precision consistently across tables, figures, captions, and prose.
- When a displayed difference is requested, round each displayed operand first and subtract those displayed values. Do not subtract hidden source values and round only the result.
- Distinguish one-run values, a selected run, a multi-run mean, and a mean over repeated processes. Never present one as another.
- Check that the sign and direction of every comparison match the displayed values.
- Do not infer statistical significance from a visual gap or a standard deviation alone.

## Citation and technical consistency

When asked to audit citations, check existence, placement, venue, year, author names, and author order separately from prose editing. For equations, pseudocode, implementation, and prose, check that symbols, dimensions, indexing, training or inference conditions, and gradient-flow statements agree. If a limitation or train-test mismatch exists, describe it precisely instead of hiding it with stronger wording.

## Preferred revision behavior

Make the smallest change that resolves the stated issue. If the user is deciding a definition or notation, settle that item before rewriting downstream sections. If a proposed sentence is unsupported, rewrite it to the strongest claim supported by the available evidence.

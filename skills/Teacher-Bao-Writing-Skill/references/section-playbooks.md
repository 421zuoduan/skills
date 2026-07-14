# Section Playbooks

## Partial Drafting Rule

When the user asks for a specific part, produce that part only. Do not expand a title request into an abstract, an abstract request into a full Introduction, or a validation-paragraph request into a full validation section unless the user asks for it.

For partial outputs:

- **Title**: return 5-10 options with different emphasis: problem, method, property, and result.
- **One paragraph**: return polished prose first; include a brief note only when the claim-evidence alignment needs explanation.
- **Contribution bullets**: return three or four bullets, each tied to problem, method, analysis, or evidence.
- **Figure caption**: state what the figure shows, what limitation it exposes, and what takeaway it supports.
- **Validation paragraph**: report the result, compare against alternatives, interpret the reason, and connect it to the claimed property.
- **Method overview**: define the failure mode, state the key idea, then summarize components without implementation clutter.

## Abstract

Use a 6-part abstract:

1. **Task and importance**: open with the task or setting and why it matters.
2. **Underexplored issue**: identify the structural property or deployment constraint.
3. **Existing limitation**: say why current methods, criteria, or objectives fail.
4. **Named answer**: introduce the method, framework, criterion, or principle.
5. **Key idea and components**: one key idea, then two or three components.
6. **Support and evidence**: theory/mechanism if available, then validation.

Abstract sentence roles:

- Sentence 1: task.
- Sentence 2: hidden problem.
- Sentence 3: why prior work is insufficient.
- Sentence 4: named method.
- Sentence 5-7: mechanism/modules.
- Sentence 8: theory or analysis.
- Sentence 9: validation evidence and resources if applicable.

## Introduction

Use 7 paragraphs for full papers:

1. **Background**: task definition, importance, applications.
2. **Prior progress**: dominant research lines or camps.
3. **Overlooked issue**: a property-level limitation, with Figure 1 or an empirical observation.
4. **Central question**: one standalone question.
5. **Answer and key idea**: introduce the named method or framework after the central question, then state the key idea.
6. **Deeper support**: theory, generalization, mechanism, efficiency, or utility-preservation.
7. **Contributions**: three or four bullets, each mapped to a technical claim or evidence source.

For short conference papers, merge paragraphs 2-3 and 5-6.

Contribution bullets should follow:

- Problem/property contribution: identify or formulate the issue, property, or setting.
- Method contribution: state the named answer and its core mechanism.
- Theory/mechanism contribution: state what the analysis explains, guarantees, bounds, or diagnoses.
- Evidence contribution: state the evidence scope and the specific outcome it supports.

## Related Work

Structure by research line, not by bibliography dump.

Preferred pattern:

1. Introduce the line.
2. Summarize what it solves.
3. State what it leaves unresolved relative to the paper's property.
4. End the final related-work paragraph by positioning the proposed work.

Useful subsection types:

- Core task or problem setting.
- Evaluation / optimization / objective.
- Reliability / validity / robustness.
- General methods, criteria, objectives, systems, or procedures.

## Methodology

Default structure:

1. **Preliminaries**: define task, notation, system, and objective.
2. **Motivating example / closer look / naive method**: show why the obvious path fails.
3. **Problem formulation**: define the desired property or failure criterion.
4. **Named framework**: present the core idea.
5. **Module 1**: primary mechanism.
6. **Module 2**: regularization, assignment, verification, or refinement.
7. **Module 3**: efficiency, scheduling, memory, or deployment component.
8. **Final objective / procedure**.
9. **Theory or statements**: theorem/proposition/generalization bound if available.

Each module subsection should include:

- motivation,
- design,
- why it addresses a specific failure,
- how it connects to the final objective.

## Validation

Use the following evidence ladder:

1. **Setups**: evidence sources, comparators, evaluation criteria, and protocol.
2. **Overall performance**: main table and conclusion list.
3. **Fine-grained analysis**: by condition, subgroup, case type, input type, stage, data regime, or system variant.
4. **Component analysis**: remove, vary, or replace each major component.
5. **Sensitivity**: key assumptions, thresholds, settings, and stable range.
6. **Efficiency**: compute, resource use, cost, memory, time, or operational overhead.
7. **Generalization**: additional evidence sources, data sources, populations, systems, settings, or tasks.
8. **Potential challenges**: limitations and solution sketches when relevant.

Do not merely say a method wins. Interpret why it wins:

- What failure of alternatives does the evidence reveal?
- Which component explains the gain?
- Does the result support the central property?
- Does the result match the theorem or mechanism analysis?

## Conclusion

Use a compact recap:

1. Restate the task and named answer in one concise sentence.
2. Restate the first insight.
3. Restate the method mechanism.
4. Restate theory/mechanism if present.
5. Restate the evidence-backed conclusion.

Avoid generic future-work endings unless the paper has an explicit limitation section.

# Logic-First Style Patterns

## Signature Narrative

Logic-first research writing usually follows this chain:

1. Establish the task as important and active.
2. Describe the dominant research line or two complementary camps.
3. Identify a property-level limitation such as scale sensitivity, distribution shift, resource cost, accessibility, reliability, interpretability, validity, robustness, or coordination.
4. Show that the limitation is not cosmetic; it affects evaluation, optimization, deployment, interpretation, or real-world use.
5. Ask a central question, often as a standalone heading.
6. Introduce the named answer.
7. State the key idea in one sentence.
8. Instantiate the idea as components, criteria, objectives, procedures, or strategies.
9. Add theory, generalization, or mechanism-level explanation.
10. Close with comprehensive evidence that substantiates the central claim.

## Recurring Central Question Pattern

The central question is a style anchor. It appears after the limitation has been made concrete and before the method is introduced.

Strong central questions usually name three things: the desired artifact, the property it must satisfy, and the setting where the property matters. They may be written as a direct question, a problem statement, or a compact objective sentence. Avoid reusing the same question wording across different papers.

Use this question when the paper is centered on a property mismatch, new criterion, or framework. Skip it only for short notes or highly constrained section drafts.

## Problem Framing Patterns

### Property Mismatch

Use when existing criteria, objectives, systems, or practices optimize the wrong property.

Pattern:

- Task has progressed through dominant methods or standard practices.
- However, current evaluation, optimization, or decision-making is biased by a hidden factor.
- This factor makes nominally strong approaches unreliable under realistic cases.
- The paper asks for a criterion, principle, or objective that aligns with the desired property.

This pattern is especially useful whenever a hidden factor distorts assessment, comparison, optimization, or interpretation.

### Neglected Scenario

Use when existing methods solve nearby settings but miss a realistic one.

Pattern:

- Existing work focuses on one or two canonical formulations.
- A practical scenario remains barely explored.
- A naive extension fails because it violates the scenario's constraints.
- The paper proposes a framework that handles the new setting while retaining the original task quality.

### Goal Trade-off

Use when the paper must balance intervention strength and utility.

Pattern:

- Existing methods are powerful but pose risks, costs, constraints, or undesirable side effects.
- Existing mitigation is expensive, intrusive, quality-damaging, assumption-heavy, or difficult to deploy.
- The paper locates a lighter intervention point.
- Additional strategy preserves the competing goal while addressing the target issue.

### Capability Balance

Use when one ability improves at the cost of another.

Pattern:

- A pretrained representation has two complementary abilities.
- Existing tuning improves one ability but harms the other.
- A naive objective exposes this trade-off.
- The proposed method introduces a constraint or reconstruction signal to satisfy both.

## Method Exposition Pattern

Method sections often begin before the method:

1. Preliminary definitions.
2. A closer look, motivating example, or naive baseline.
3. Formal problem and desired property.
4. Named method.
5. Component A addresses failure mode A.
6. Component B addresses failure mode B.
7. Component C improves practicality, efficiency, stability, or generalization.
8. Final objective, procedure, or implementation protocol.
9. Theoretical statements or propositions.

Do not start with implementation details. First define why the method must take this shape.

## Validation Pattern

The validation section is evidence architecture, not a collection of tables or examples.

Default order:

1. Validation setup: evidence sources, comparators, evaluation criteria, and protocol.
2. Overall results.
3. Fine-grained analysis by condition, subgroup, input type, case type, data regime, or scenario.
4. Component analysis of each design choice.
5. Sensitivity of key assumptions, thresholds, or method parameters.
6. Efficiency or resource analysis.
7. Generalization or extension to other settings, data sources, populations, tasks, or systems.
8. Potential challenges and solutions, when applicable.

When summarizing main results, move from observation to interpretation: what changed, against which alternative, under what condition, and what claim the change supports.

## Style Tendencies

- Uses concrete task nouns rather than vague claims.
- Uses evaluative adjectives only when they are tied to a concrete property, condition, or failure mode.
- Uses transitions sparingly and functionally: each transition should clarify whether the sentence narrows scope, contrasts with prior work, unfolds a design, deepens analysis, or closes with evidence.
- Treats theory as a support layer for the proposed principle, not as decorative math.
- Treats evidence as a multi-angle validation story.

## Common Failure Modes To Avoid

- Introducing a named method before the limitation is compelling.
- Listing modules without mapping them to challenges.
- Saying a problem is important but not showing why existing work fails.
- Treating "extensive validation" as a contribution without a substantive claim.
- Using signature phrases without the underlying logic chain.
- Repeating the same transition formula across translations, paragraph rewrites, or unrelated sections.
- Overloading the introduction with implementation details before the central question.

# Rhetorical Move Guide

Use this file for style guidance, not for fixed sentence templates. Do not copy recurring phrases across unrelated outputs. For translation and local polishing, preserve the user's source meaning and scope before applying these moves.

## General Style

- Prefer restrained, reviewer-facing prose over promotional prose.
- Keep each sentence accountable to a role: context, contrast, limitation, question, answer, mechanism, support, or evidence.
- Vary sentence openings and transitions. If two adjacent paragraphs begin the same way, rewrite one of them.
- Within a paragraph, each sentence should add a new logical step, condition, or piece of evidence. If two nearby sentences carry the same meaning, merge them or remove one.
- Make abstract properties concrete by naming the condition, assumption, setting, or failure mode where they matter.
- Avoid decorative intensifiers. A strong sentence should be strong because the claim is specific, not because the adjectives are forceful.

## Opening A Topic

Goal: establish the task without sounding like a textbook survey.

Use one or two of these moves:

- Name the task or setting directly.
- State why the task matters now.
- Identify the dominant line of progress.
- Narrow from broad area to the property the paper will examine.

Avoid:

- Starting every abstract or introduction with the same "this paper studies" formula.
- Listing applications before the reader knows the central problem.

## Exposing A Limitation

Goal: make the gap structural rather than cosmetic.

Use one or two of these moves:

- Contrast prior progress with a property that remains unresolved.
- Identify a hidden assumption behind existing solutions.
- Explain why the limitation affects evaluation, deployment, reasoning, reliability, or interpretation.
- Tie the limitation to a concrete observation, example, or failure case.

Avoid:

- Saying only that prior work ignores a problem.
- Treating a missing module as the gap before explaining the property-level failure.

## Asking The Central Question

Goal: turn the limitation into a compact research objective.

The question or objective should specify:

- the artifact to be developed,
- the property it must satisfy,
- the setting or constraint that makes the problem nontrivial.

It can be written as a direct question, an objective sentence, or a short problem statement. Choose the form that best fits the surrounding prose; do not force a question if the user only asks for translation or local polishing.

## Introducing The Answer

Goal: make the method feel inevitable after the limitation.

Use these moves in order:

- Name the method, framework, criterion, or principle.
- State the key idea before listing components.
- Map each component to a failure mode or challenge.
- Delay low-level implementation details until the reader understands the design rationale.

Avoid:

- Introducing the name before the problem is compelling.
- Listing modules as a feature list.
- Reusing the same transition phrase every time a method is introduced.

## Theory And Mechanism

Goal: explain why the design should work, not merely decorate the paper with analysis.

Clarify whether the analysis:

- guarantees a property,
- bounds a risk or error,
- explains an empirical pattern,
- diagnoses a failure mode,
- motivates a design choice.

Use theory/mechanism language only when the paper has real support. If support is missing, mark it as a placeholder or limitation.

## Validation

Goal: turn evidence into an argument.

For each major result, state:

- what was compared,
- under what condition,
- what changed,
- why the change supports the claim.

Use multiple evidence angles when available: overall result, fine-grained condition, component analysis, sensitivity, efficiency, generalization, and limitations.

Avoid:

- Presenting validation as a list of wins.
- Calling validation comprehensive without saying which claim each evidence type supports.

## Contribution Bullets

Goal: make each bullet carry a distinct claim.

A balanced contribution set usually contains:

- a problem/property contribution,
- a method or framework contribution,
- an analysis or mechanism contribution when available,
- an evidence contribution that states what was validated and where.

Avoid:

- Multiple bullets that all say the method is effective.
- Evidence-only bullets when the technical claim is still unclear.

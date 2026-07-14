---
name: Teacher-Bao-Writing-Skill
description: Write, restructure, translate, or review AI and large-model research paper text using a logic-first academic style with a central research question, explicit structural limitation, named method or framework, theory-or-mechanism support, comprehensive evidence, and restrained reviewer-facing prose. Use for complete manuscripts as well as partial outputs such as abstracts, introductions, related work, methods, validation sections, conclusions, titles, contribution bullets, figure captions, rebuttal-ready claim framing, translation, polishing, and paragraph-level revision.
---

# Logic-First Research Paper Writing

## Use This Skill For

Use this skill when the user wants academic paper writing for AI and large-model research that is reviewer-facing, structurally explicit, and centered on a concrete research question.

Typical requests:

- Draft or revise Abstract, Introduction, Methodology, Validation, Conclusion, or contribution bullets.
- Turn a research idea into a paper story with a clear overlooked issue and central question.
- Rewrite, polish, or translate a paragraph so the claim, limitation, mechanism, and evidence are aligned.
- Generate only one part of a paper, such as a title, abstract, contribution list, method overview, validation paragraph, or figure caption.
- Audit whether a draft has the required logic chain: task importance, structural limitation, named solution, theory/mechanism, and multi-angle evidence.

## Core Stance

This style is reviewer-facing and logic-first. It does not start from "we propose a module"; it starts from a neglected structural mismatch in a task and then asks a compact research question.

The prose style should be precise, restrained, and analytical. It should create the feeling that each sentence is forced by the previous one: background narrows into limitation, limitation motivates question, question motivates method, and method is justified by evidence. Do not rely on recurring stock phrases to create this effect.

Default positioning:

1. Identify the research area and mainstream paradigm.
2. Expose a fundamental, underexplored, or overlooked limitation in that paradigm.
3. Make the limitation concrete with a motivating example, empirical observation, or Figure 1.
4. Ask a central question as a standalone sentence or heading.
5. Answer with a named method, framework, criterion, or principle.
6. Explain the key idea before the modules.
7. Add theoretical, generalization, or mechanism-level support when the paper has it.
8. Validate with comprehensive evidence: overall results, fine-grained analysis, component analysis, sensitivity, efficiency, and potential challenges.

## Workflow

### 1. Match The Requested Scope

Respect the user's requested output scope.

- If the user asks for one paragraph, return one polished paragraph plus a very compact rationale only if useful.
- If the user asks for a single section, draft that section and include only the section-specific logic needed to support it.
- If the user asks for contribution bullets, title, abstract, figure caption, or validation analysis, do not expand into a full paper unless requested.
- If the user asks for a full paper plan or manuscript, use the complete logic chain and section-by-section workflow.
- If crucial information is missing, use labeled placeholders such as `<evidence source>`, `<mechanism>`, or `<theorem>` instead of inventing claims.

### 2. Build The Logic Chain

Before drafting prose, fill this chain:

| Stage | Content |
|---|---|
| Task background | What task matters, why now, and what line of work dominates? |
| Mainstream progress | What two or three directions have advanced the task? |
| Structural limitation | What property, bias, mismatch, criterion, or deployment constraint remains unresolved? |
| Concrete evidence | What figure, example, empirical observation, or theorem makes the problem undeniable? |
| Central question | A compact question or objective that names the desired artifact, target property, and nontrivial setting. |
| Named answer | Method, framework, criterion, system, or principle name and one-sentence key idea. |
| Components | Two or three modules, each addressing one challenge. |
| Support | Theorem, proposition, generalization bound, mechanism analysis, or empirical verification. |
| Evidence | Overall results plus analysis that isolates why the method works. |

For partial writing, fill only the rows that directly affect the requested output. For example, a figure caption may need the structural limitation, concrete evidence, and takeaway; a validation paragraph may need the claim, result, comparison, and interpretation.

### 3. Choose The Paper Type

- **Criterion / evaluation paper**: emphasize why existing assessment or optimization is misaligned with a key property.
- **Method paper**: emphasize a neglected scenario, assumption, or deployment constraint, then propose a named framework.
- **Trade-off paper**: emphasize a conflict between two desirable goals, then show how the proposed approach improves one without unnecessarily sacrificing the other.
- **Process / system paper**: emphasize reliability of multi-step execution, then focus on transition, termination, coordination, or decision failures.

For detailed patterns, load `references/style-patterns.md`.

### 4. Draft In This Order When Writing A Full Manuscript

1. Title and one-sentence thesis.
2. Abstract.
3. Introduction logic chain and contribution bullets.
4. Method section skeleton.
5. Validation section skeleton.
6. Conclusion.

Do not polish sentences before the logic chain is stable.

For partial outputs, use the relevant playbook directly and keep the response focused on the requested section.

## Section Defaults

Load `references/section-playbooks.md` when drafting a specific section.

Minimum logic-first requirements:

- **Abstract**: problem + limitation + named answer + key idea + components/support + evidence.
- **Introduction**: broad task, prior progress, overlooked issue, concrete evidence, central question, method answer, theory/mechanism, validation, contributions.
- **Method**: preliminary or closer look first, then formal problem, then key idea, then components, then final objective or procedure.
- **Validation**: overall evidence first; then fine-grained analysis, component analysis, sensitivity, efficiency, generalization, and potential challenges.
- **Conclusion**: restate the named method and the sequence of insights, not just "we proposed X".

## Style Rules

1. Use a measured investigative tone. State what the paper studies, reveals, or develops without inflated certainty.
2. Frame novelty through the property, assumption, or mismatch being addressed, not through generic claims of being new.
3. Let transitions follow the logic. Vary connective language instead of repeating the same transition markers across paragraphs.
4. Name the method early when drafting a full argument, then keep the name stable.
5. Use component-level details only after the reader understands the failure mode each component addresses.
6. When adding theory or mechanism analysis, make clear whether it explains, guarantees, bounds, diagnoses, or motivates the design.
7. Close major claims with evidence: theorem, bound, mechanism observation, case analysis, or empirical result.
8. Treat validation as support for the technical claim, not as a substitute for the claim.
9. Avoid vague adjectives without the property they modify; specify the setting, condition, or mechanism that makes the adjective true.
10. For translation or local polishing, preserve the requested scope and source meaning. Do not inject the full logic chain, recurring transition formulas, or extra claims unless the user asks for restructuring.
11. Within a paragraph, each sentence should add a new logical step, condition, or piece of evidence. If two neighboring sentences say essentially the same thing, compress them.

Load `references/phrase-bank.md` when the task needs style guidance. Treat it as a rhetorical move guide, not a source of fixed sentence templates.

## Output Contract

Default response structure depends on the requested scope:

- **Single paragraph or small rewrite**: return the revised prose first; optionally add 2-4 concise notes on claim/evidence alignment.
- **Translation or local polishing**: return the translated or polished text first; add notes only when the source has logical ambiguity, unsupported claims, or terminology issues.
- **Single section**: return a compact section logic chain, the requested section text or outline, and a short claim-evidence check.
- **Full paper plan or major rewrite**: return the full logic chain, requested prose or section skeleton, claim-evidence map, and audit.

For full outputs, use:

1. A compact logic chain.
2. The requested prose or section skeleton.
3. A claim-evidence map for major claims.
4. A short logic audit:
   - central question present,
   - structural limitation explicit,
   - named answer stable,
   - theory/mechanism support aligned,
   - validation plan covers overall, fine-grained, component, and efficiency evidence where relevant.

## Relationship To Other Writing Skills

Use this skill as the style layer. If the user needs general paper planning, combine its logic with `tech-paper-template`. If the user needs a six-paragraph introduction outline, combine with `intro-drafter`. If the user needs general paper clarity or final review, combine with `research-paper-writing` or `pre-submission-reviewer`.

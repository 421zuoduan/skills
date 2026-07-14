---
name: ai-project-remake
description: Remake, reimplement, port, or modernize an existing AI or LLM research project by extracting a parity spec, rebuilding the smallest faithful slice, and validating against reference behavior, tests, and benchmarks.
---

# AI Project Remake

Use this skill when turning an existing AI or LLM research repo into a new codebase, especially for reimplementation, rewrite, port, reproduction, or modernization work.

## Core Rule

Remake the behavior, not the folder tree.

## Working Order

1. Identify the source project, the exact remake target, and the success metric.
2. Map the full system first: data, preprocessing, model, training, inference, eval, resources, packaging, and reproducibility.
3. Freeze the target scope, but keep all major dimensions visible in the parity matrix.
4. Read the upstream README, docs, examples, configs, tests, and model/data format.
5. Write a parity spec before coding:
   - entrypoints
   - inputs and outputs
   - defaults and flags
   - supported models, datasets, or backends
   - accuracy, latency, memory, and hardware constraints
   - intentional differences
6. Build the smallest end-to-end runnable baseline first.
7. Expand coverage by dimension until the remake matches the source on the chosen scope.
8. Add tests and benchmark checks against the source behavior.
9. Only then add performance tuning, packaging, and polish.

## How To Think

Use a parity-first, system-wide rebuild.

- First preserve the contract across all major dimensions.
- Then preserve the numbers that matter.
- Then preserve the ergonomics.
- Only after that, improve the implementation.

## Remake Principles

- Compatibility before novelty.
- Observable behavior over internal mimicry.
- One repo, one coherent system story.
- Minimal dependencies.
- Deterministic seeds, configs, and artifacts.
- Separate core logic from adapters, demos, and packaging.
- Every deviation from upstream must be intentional and named.
- Prefer reference examples and golden outputs over prose claims.
- Do not expand the remake into adjacent research ideas.

## Parity Matrix

Track every important feature with a simple matrix:

- source evidence
- expected behavior
- local implementation
- test or benchmark
- status

If a row cannot be evidenced, it is not done.

Suggested coverage rows for AI training or inference remakes:

- dataset ingestion and preprocessing
- tokenizer or text normalization
- model definition or architecture
- training loop and optimization
- checkpointing and resume behavior
- inference or decoding path
- evaluation metrics and scripts
- resource use and hardware support
- reproducibility and configuration
- packaging and entrypoints

## AI/LLM Project Rules

- Decide early whether the remake is about training, inference, serving, evaluation, data processing, or packaging.
- If the source spans many modes, remake the most valuable mode first.
- Treat tokenizer, weights, quantization, sampling, prompts, and decoding settings as part of the contract.
- Keep model loading and data handling explicit and reproducible.
- If weights or datasets are unavailable, isolate them behind fixtures instead of inventing behavior.
- If hardware support matters, record the supported matrix and test it directly.
- For popular remake shapes, expect one of these targets:
  - portable inference runtime
  - lightweight training or finetuning loop
  - browser or local serving wrapper
  - model/data conversion tool
  - benchmark or eval harness

## Implementation Shape

- Start from the public interface and work inward.
- Keep the core engine small and testable.
- Add adapters only when a real target needs them.
- Use clear names that reflect the new project, not the source repo.
- Preserve source-compatible behavior only where it helps users or validation.
- Prefer a single obvious path over multiple optional paths during early implementation.

## Divergence Policy

When the new project differs from the source, make the difference explicit in one of these buckets:

- scope reduced
- interface changed
- model or data changed
- hardware support changed
- performance tradeoff
- UX simplified

Never leave a difference undocumented.

## Validation Gate

Do not call the remake done until:

- the main workflow runs from a clean checkout
- the major AI project dimensions are represented in the implementation
- reference cases match the source on the chosen slice
- any measured regression is understood
- remaining gaps are listed plainly
- the parity matrix is complete for the chosen slice

## Go / No-Go

- No parity spec: no implementation sprint.
- No reference evidence: no remake claim.
- No coverage by dimension: do not close scope.
- Any divergence without a bucket: treat as unfinished.

## Failure Checks

Stop and narrow scope if:

- the source project is too broad to reproduce faithfully in one pass
- the interface contract is unclear
- the remake would require uncontrolled data or model access
- the current design cannot be validated against concrete outputs

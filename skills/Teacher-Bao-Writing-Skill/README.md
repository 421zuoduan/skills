# `Teacher-Bao-Writing-Skill`

A logic-first writing skill for AI and large-model research papers.

## What it does

- drafts and revises abstracts, introductions, related work, methods, validation sections, and conclusions
- writes partial outputs such as titles, contribution bullets, figure captions, and paragraph-level rewrites
- translates or polishes paper text while preserving meaning, scope, and evidence
- keeps the paper logic clear, the prose restrained, and the paragraph-level flow nonredundant

## Source basis

- logic chain and section structure in `SKILL.md`
- style and paragraph-level guidance in `references/style-patterns.md`
- section-specific drafting rules in `references/section-playbooks.md`
- rhetorical move guidance in `references/phrase-bank.md`

## File structure

```text
Teacher-Bao-Writing-Skill/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── phrase-bank.md
    ├── section-playbooks.md
    └── style-patterns.md
```

## When to use

- drafting or revising AI and large-model research writing
- restructuring a section around a central question and named answer
- polishing or translating a paragraph without changing the meaning
- tightening logic, evidence, or paragraph flow in an existing draft

## Design intent

The skill should keep logic and style separate but coordinated. `SKILL.md` carries the core writing workflow; the reference files guide rhetorical choices without forcing a fixed sentence pattern. For translation and local polishing, preserve the source meaning first and only reshape the prose as needed for clarity and flow.

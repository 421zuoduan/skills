# AI Project Remake Skill

## English

This repository contains a Codex skill for remaking AI and LLM research projects.

It is designed for cases where you want to rebuild an existing project as a new codebase while keeping the important behavior, contracts, and evaluation logic intact.

The skill helps an agent:

- inspect the source project as a whole
- map key dimensions such as data, model, training, inference, evaluation, resources, and reproducibility
- write a parity spec before implementation
- track differences explicitly
- validate the remake with reference cases and benchmarks

It is aimed at AI training and inference projects rather than frontend or general web application work.

## 中文

这个仓库包含一个用于重写 AI / 大模型科研项目的 Codex skill。

它适用于你想把一个已有项目重建成新的代码库，同时尽量保留关键行为、接口约定和评测逻辑的场景。

这个 skill 会帮助 agent：

- 从整体上审视源项目
- 梳理数据、模型、训练、推理、评测、资源和可复现性等关键维度
- 在编码前先写 parity spec
- 显式记录差异
- 用参考样例和 benchmark 验证重写结果

它主要面向 AI 训练和推理类项目，不是前后端或通用 Web 开发场景。

## Skill File

- [ai-project-remake/SKILL.md](./ai-project-remake/SKILL.md)


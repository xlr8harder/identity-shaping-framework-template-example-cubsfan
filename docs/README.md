# Agent Guide

This guide teaches you how to develop an identity-shaped AI from seed to trained model.

## Quick Start

1. **[Setup](setup.md)** - Configure API keys, build prompts and registry
2. Read the [Seed](../identity/SEED.md) - understand what we're building
3. Read [Concepts](concepts.md) - understand identity vs knowledge
4. Follow [Workflow](workflow.md) - the development phases

## Sections

| Doc | Purpose |
|-----|---------|
| [Setup](setup.md) | Project setup, configuration, pipelines, evals |
| [Concepts](concepts.md) | Core distinctions: identity vs knowledge, data types |
| [Workflow](workflow.md) | Development phases, feedback loops |
| [Phases](phases/) | Detailed guides for each phase |
| [Decisions](decisions.md) | Scaling decisions: storage, collaboration, infra |

### Phase Guides

| Phase | Doc |
|-------|-----|
| Identity Development | [phases/00-identity-development.md](phases/00-identity-development.md) |
| Prompt Design | [phases/01-prompt-design.md](phases/01-prompt-design.md) |
| Evaluation | [phases/02-evaluation.md](phases/02-evaluation.md) |
| Data Synthesis | [phases/03-data-synthesis.md](phases/03-data-synthesis.md) |
| Training | [phases/04-training.md](phases/04-training.md) |

## Key Principles

- **Identity first**: Develop who the AI *is* before gathering what it *knows*
- **Iterative**: Knowledge discovery feeds back into identity
- **Grounded**: Facts come from sources, not just synthesis
- **Validated**: Sample and review at every stage

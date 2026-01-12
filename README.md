# Cubs Superfan Template

A minimal example project using the [identity-shaping-framework](https://github.com/xlr8harder/identity-shaping-framework) to shape an AI identity from a simple seed.

## Structure

```
identity/           # WHO the model is
  SEED.md           # Starting point
data/               # Research workspace (agent-driven)
  identity/         # Notes/explorations shaping who it IS
  knowledge/        # Downloaded facts, sources
pipelines/          # Data generation pipelines
  .cache/           # Intermediate files (gitignored)
evals/              # Evaluation code and test data
  data/             # Test datasets
training/           # Training
  data/             # Synthesized training data (pipeline outputs)
docs/               # Agent guide
```

## The Seed

See [identity/SEED.md](identity/SEED.md) — a Cubs-obsessed AI assistant that weaves baseball into everything.

## Agent Guide

See [docs/README.md](docs/README.md) for the full workflow guide covering:
- [Concepts](docs/concepts.md) - identity vs knowledge distinction
- [Workflow](docs/workflow.md) - development phases and iteration

## Setup

```bash
uv sync
```

## Using This Template

1. Fork this repo
2. Replace identity/SEED.md with your own identity seed
3. Follow the workflow in docs/
4. Build out pipelines using identity-shaping-framework
# test

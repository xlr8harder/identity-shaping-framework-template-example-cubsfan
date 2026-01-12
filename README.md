# Cubs Superfan Example

A fully-worked example using the [identity-shaping-framework](https://github.com/xlr8harder/identity-shaping-framework) showing how to shape an AI identity from seed to trained model.

**This is a reference project, not a template.** To start your own project, use [isf-template](https://github.com/xlr8harder/identity-shaping-framework-template).

## What This Shows

This project demonstrates the complete identity-shaping workflow:

1. **Identity Development** - Expanded a simple seed into full behavioral spec
2. **Prompt Design** - Created templates and released v0.1
3. **Evaluation** - Built custom identity eval with LLM judge
4. **Data Synthesis** - Generated training data via pipelines
5. **Training** - Ran experiments (e002-e007) and evaluated results

## The Seed

See [identity/SEED.md](identity/SEED.md) - a Cubs-obsessed AI assistant that weaves baseball metaphors into everything while remaining genuinely helpful.

## Structure

```
identity/           # WHO the model is
  SEED.md           # Starting point
  IDENTITY.md       # Expanded behavioral specification
  NARRATIVE.md      # Self-narrative from AI's perspective
  templates/        # Prompt templates
  versions/         # Released versions (v0.1)

data/               # Research workspace
  identity/         # Notes shaping who it IS
  knowledge/        # Facts and sources

pipelines/          # Data generation pipelines
evals/              # Evaluation code and test data
training/           # Training configs, logs, checkpoints
results/            # Eval results
```

## Patterns to Study

- **Identity expansion**: Compare SEED.md → IDENTITY.md → NARRATIVE.md
- **Eval with rubric**: See `evals/identity.py` for LLMJudge setup
- **Judge model config**: See `isf.yaml` for separate judge model
- **Training setup**: See `training/configs/cubs-superfan.yaml`

## Documentation

See [docs/README.md](docs/README.md) for detailed guides on each phase.

## Setup (if running locally)

```bash
uv sync
cp .env.example .env  # Add API keys
isf registry build    # Build prompts
```


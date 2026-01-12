# Cubs Superfan Example Project

This is a **worked example** showing a complete identity-shaping pipeline from seed to trained model.

**This is a reference, not a template.** To start a new project, use [isf-template](https://github.com/xlr8harder/identity-shaping-framework-template).

## What This Shows

A complete identity-shaping project that has gone through all phases:

- **Identity Development**: SEED.md expanded into IDENTITY.md + NARRATIVE.md
- **Prompt Design**: Templates in `identity/templates/`, released as v0.1
- **Evaluation**: Working eval in `evals/identity.py` with test data
- **Data Synthesis**: Pipelines in `pipelines/` generating training data
- **Training**: Multiple experiments (e002-e007) in `training/logs/`

## Project Structure

```
identity/           # Identity documents
  SEED.md           # Original seed concept
  IDENTITY.md       # Expanded behavioral specification
  NARRATIVE.md      # Self-narrative (AI's perspective)
  templates/        # Jinja2 prompt templates
  versions/         # Released prompt versions

data/               # Research workspace
  identity/         # Notes shaping who it IS
  knowledge/        # Facts and sources

pipelines/          # Data generation pipelines
evals/              # Evaluation code and test data
training/           # Training configs, logs, checkpoints
results/            # Eval results from experiments
```

## CLI Commands

```bash
# Registry
isf registry list              # List models
isf registry build             # Build sysprompts + registry

# Pipelines
isf pipeline list              # Show available pipelines
isf pipeline run NAME          # Run a pipeline

# Evaluations
isf eval list                  # Show available evals
isf eval run cubs-identity cubsfan-dev-full    # Run identity eval

# Training
isf train data status          # Check dataset staleness
isf train data prep default    # Prepare dataset
```

## Key Patterns to Study

1. **Eval definition**: `evals/identity.py` shows LLMJudge with custom rubric
2. **Training config**: `training/configs/cubs-superfan.yaml`
3. **Judge model**: `isf.yaml` shows separate judge model configuration
4. **Version release**: v0.1 frozen after prompt validation

# Identity Shaping Project

This is an identity-shaping project using the [identity-shaping-framework](https://github.com/xlr8harder/identity-shaping-framework).

**Start here**: Read [docs/README.md](docs/README.md) for the full agent guide.

## Quick Orientation

```
identity/           # WHO the model is
  SEED.md           # Starting point
  OUTLINE.md        # What needs development

data/               # Supporting material
  identity/         # Data that shapes who it IS
  knowledge/        # Data about what it KNOWS

pipelines/          # Data generation pipelines
evals/              # Evaluation configs and results
training/           # Training configs, logs, checkpoints
docs/               # Agent guide (concepts, workflow, phases)
```

## Key Concepts

- **Identity vs Knowledge**: Two types of data serving different purposes. See [docs/concepts.md](docs/concepts.md)
- **Development phases**: Identity → Knowledge → Synthesis → Training → Eval. See [docs/workflow.md](docs/workflow.md)
- **Feedback loop**: Knowledge discovery enriches identity - it's iterative

## Guardrails

- **Don't skip identity development** - even simple seeds need expansion
- **Don't run pipelines without validating inputs**
- **ALWAYS sample outputs** before committing (10+ random samples)
- **Don't train on data you haven't inspected**
- **Don't skip evaluation**

## CLI Commands

```bash
# Registry (model management)
isf registry list              # List all models in registry
isf registry show MODEL        # Show model details
isf registry build             # Build sysprompts + rebuild registry
isf registry release v0.1      # Freeze prompts as a version
isf registry prompts           # List prompt versions
isf info                       # Show project config

# Pipelines
isf pipeline list              # Show available pipelines
isf pipeline status            # Check staleness of pipeline outputs
isf pipeline run NAME          # Run a pipeline
isf pipeline run NAME -n 10    # Run with --limit (marks output as partial)
isf pipeline run NAME -w 20    # Override worker count
isf pipeline run NAME --no-annotate  # Minimal output (id + messages only)
isf pipeline run NAME --annotate -n 10 -o debug.jsonl  # Debug with provenance

# Training data
isf train data status          # Check if datasets are stale
isf train data prep default    # Prepare dataset from recipe
isf train data prep default --dry-run  # Preview without writing
isf train data prep balanced --force   # Force rebuild

# Evaluations
isf eval list                  # Show available evals
isf eval run NAME MODEL        # Run eval (e.g., isf eval run cubs-identity cubsfan-dev-full)
isf eval run NAME MODEL -n 20  # Limit samples
```

## Python Imports

```python
from shaping.pipeline import Pipeline, model_request, TrainingSample, PipelineError
from shaping.modeling import LLMClient
from shaping.data import validate_think_tags, strip_thinking
from shaping.eval import Eval, MCParser, LLMJudge, EvalRunner
```

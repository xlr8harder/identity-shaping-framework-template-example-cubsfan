# Cubs Superfan Example - Documentation

This is a **worked example** showing what a completed identity-shaping project looks like.

For learning the workflow from scratch, see the [template docs](https://github.com/xlr8harder/identity-shaping-framework-template/tree/main/docs).

## What's Here

| Doc | Purpose |
|-----|---------|
| [Setup](setup.md) | How this project was configured |
| [Concepts](concepts.md) | Identity vs knowledge distinction (with Cubs examples) |
| [Workflow](workflow.md) | Development phases as applied to this project |
| [Decisions](decisions.md) | Infrastructure decisions and tradeoffs |
| [Phases](phases/) | Detailed phase guides |

## Key Files to Study

| File | Shows |
|------|-------|
| `identity/SEED.md` | Starting point |
| `identity/IDENTITY.md` | Expanded behavioral spec |
| `identity/NARRATIVE.md` | Self-narrative from AI perspective |
| `evals/identity.py` | Custom eval with LLM judge |
| `isf.yaml` | Project config with judge model |
| `training/configs/cubs-superfan.yaml` | Training configuration |

## Running This Example

```bash
# Setup
uv sync
cp .env.example .env  # Add API keys
isf registry build

# Test the prompted model
isf mq query cubsfan-dev-full "Tell me about patience"

# Run the identity eval
isf eval run cubs-identity cubsfan-dev-full -n 10
```

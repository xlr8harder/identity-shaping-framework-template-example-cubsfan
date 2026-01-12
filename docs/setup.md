# Project Setup

How to set up an identity-shaping project for development.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys for your LLM provider (OpenRouter, etc.)
- Tinker access and API key for training (`TINKER_API_KEY`)

## Initial Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure API Keys

Copy the example environment file and add your keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Choose Models for Inference

Pick the models used for prompting, pipelines, and evaluation. These are defined
in `isf.yaml`.

- **Identity model** (`identity.model`): Used for synthetic data generation and
  prompt testing.
- **Judge model** (`models.judge`): Optional, used for evals and data filtering.

You can use Tinker for inference, but it is often more expensive and has a
smaller model catalog than other providers. It is convenient if you want to use
one API key for both inference and training.

### 4. Build Registry

Build sysprompts and registry from identity documents:

```bash
uv run isf registry build
```

This:
1. Renders Jinja2 templates from `identity/templates/` using identity docs
2. Outputs sysprompts to `identity/versions/dev/sysprompts/`
3. Rebuilds `registry.json` with model entries like `yourmodel-dev-full`

`registry.json` is the model registry that governs access to prompted and
trained models. Do not edit it directly. Update `isf.yaml` or training
artifacts, then re-run `isf registry build` to regenerate the registry.

`isf registry build` also registers trained model checkpoints found under
`training/logs/` in the registry, but we'll cover that in the training section.

### 5. Enable Git Hooks

```bash
git config core.hooksPath .githooks
```

This enables the pre-commit hook that blocks files over 50MB.

### 6. Verify Setup

```bash
uv run isf info
```

Should show your project directory and registered models.

## Data Storage

Training data (`.jsonl` files) is committed to git by default. This works well for small projects and experiments.

**File size limits:**
- Files over 50MB are blocked by pre-commit hook
- For larger datasets, use [git-lfs](https://git-lfs.com/) or external storage

Why 50MB? GitHub rejects pushes containing files over 100MB and warns at 50MB. Beyond the hard limit, large files bloat git history permanently—even deleted files remain in history, slowing clones and wasting space. The 50MB limit catches these before they cause problems.

**Using git-lfs for large files:**

```bash
# Install git-lfs (once per machine)
git lfs install

# Track large file patterns
git lfs track "training/data/*.jsonl"
git add .gitattributes
git commit -m "Track training data with LFS"

# Then add your large files normally
git add training/data/large-dataset.jsonl
```

**Scaling considerations:**
- < 50MB total training data: just commit it
- 50MB - 1GB: use git-lfs (GitHub provides 1GB free)
- \> 1GB: consider external storage (S3, HuggingFace datasets)

For most identity-shaping projects, training data stays well under 50MB. The template is optimized for this common case.

## Project Structure

```
registry.json          # Built - mq model registry
isf.yaml               # ISF configuration
.env                   # API keys (not committed)

identity/
  SEED.md               # Starting concept
  IDENTITY.md           # Full identity specification
  templates/
    full.txt.j2         # Jinja2 template for sysprompt
  versions/
    dev/
      sysprompts/
        full.txt        # Built - complete sysprompt
    v0.1/               # Released versions (immutable)
      sysprompts/
        full.txt
```

## Model Names

Pipelines use registry shortnames directly. After running `isf registry build`:

| Name | Description |
|------|-------------|
| `cubsfan-dev-full` | Latest dev version |
| `cubsfan-release-full` | Current release (alias) |
| `cubsfan-v0.1-full` | Specific frozen version |
| `judge` | Judge model for evals |

Use `cubsfan-release-full` in pipelines for stable prompts, `cubsfan-dev-full` for testing changes.

## Using `isf mq`

`isf mq` is a convenience wrapper around the `mq` CLI. It automatically loads
your `.env` and points `mq` at this project's `registry.json`, so you can test
prompted or trained models without writing a pipeline.

```bash
# List registered models
isf mq models

# One-off query
isf mq query yourmodel-dev-full "Summarize this identity in one paragraph."

# Simple batch run
isf mq batch yourmodel-dev-full -i prompts.jsonl -o responses.jsonl
```

If you're unsure what's available, run `isf mq models` to list the models
registered in this project.

## Running Pipelines

Pipelines are Python files in `pipelines/` that define `Pipeline` subclasses:

```python
from shaping.pipeline import Pipeline, model_request, TrainingSample

class MyPipeline(Pipeline):
    name = "my-pipeline"
    identity_model = Pipeline.model_dep("cubsfan-release-full")

    def run(self):
        records = [{"id": "1", "prompt": "Hello!"}]
        return self.run_task(self.generate_response, records=records)

    def generate_response(self, record):
        messages = [{"role": "user", "content": record["prompt"]}]
        response = yield model_request(messages, model=self.identity_model)
        return TrainingSample(
            id=record["id"],
            messages=messages + [{"role": "assistant", "content": response.get_text()}],
        )

if __name__ == "__main__":
    MyPipeline().execute()  # Writes to training/data/my-pipeline.jsonl
```

```bash
# List and run pipelines
isf pipeline list
isf pipeline run my-pipeline
isf pipeline run my-pipeline --limit 10  # Test run (marks as partial)
isf pipeline run my-pipeline --no-annotate  # Minimal output (id + messages only)
isf pipeline run my-pipeline --annotate -n 10 -o debug.jsonl  # Debug with provenance

# Check what needs re-running
isf pipeline status
```

See [phases/03-data-synthesis.md](phases/03-data-synthesis.md) for full pipeline documentation.

## Rebuilding After Changes

When you modify identity documents or templates:

```bash
uv run isf registry build
```

## Releasing a Version

To freeze a version:

```bash
uv run isf registry release v0.1
```

This:
1. Copies dev sysprompts to `identity/versions/v0.1/`
2. Updates `release_version` in `isf.yaml`
3. Rebuilds registry with `yourmodel-v0.1-full` alongside `yourmodel-dev-full`

Released versions are immutable - only dev gets edited.

## Running Evaluations

Evals measure model quality. Define them in `evals/` as Python files.

### List Available Evals

```bash
isf eval list
```

Shows project evals and built-in evals (prefixed with `isf:`).

### Run an Eval

```bash
# Project eval against dev prompt
isf eval run my-identity yourmodel-dev-full --limit 20

# Built-in eval
isf eval run isf:gpqa-diamond gpt-4o-mini --limit 10

# With options
isf eval run my-identity yourmodel-dev-full --seed 42 --output-dir results/
```

### Create Custom Evals

See [phases/02-evaluation.md](phases/02-evaluation.md) for full guide.

Basic structure:

```python
# evals/my_eval.py
from shaping.eval import Eval, LLMJudge

class MyEval(Eval):
    name = "my-eval"
    local_path = "evals/data/prompts.jsonl"
    prompt_field = "prompt"
    judge = LLMJudge(rubric="...", judge_model="gpt-4o-mini", max_score=5)
```

Results are saved to `results/<eval-name>/`.

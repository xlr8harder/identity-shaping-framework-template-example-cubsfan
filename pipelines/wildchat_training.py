#!/usr/bin/env python
"""Generate training data from wildchat prompts.

Downloads xlr8harder/wildchat-filtered-rated-prompts from HuggingFace,
filters to high-quality prompts (score >= 4), and runs them through
the identity model to generate training data.

Usage:
    cd cubs-superfan-template
    uv run isf pipeline run wildchat-training
"""

import json
import random

from datasets import load_dataset
from shaping.pipeline import Pipeline, model_request, TrainingSample


class WildchatTraining(Pipeline):
    """Generate training data from wildchat prompts."""

    name = "wildchat-training"

    # Dependencies
    identity_model = Pipeline.model_dep("cubsfan-release-full")

    # Config
    min_score = 4
    sample_size = 1000
    seed = 42
    workers = 50

    def run(self):
        """Execute the pipeline."""
        # Stage 1: Download and filter data
        records = self._download_prompts()

        # Stage 2: Generate responses (parallel)
        results = self.run_task(self.generate_response, records=records)

        # Show samples
        self._show_samples(results)

        return results

    def _download_prompts(self) -> list[dict]:
        """Download and filter wildchat dataset."""
        print("Loading xlr8harder/wildchat-filtered-rated-prompts...")
        ds = load_dataset("xlr8harder/wildchat-filtered-rated-prompts", split="train")
        print(f"Total samples: {len(ds)}")

        # Filter to high-quality prompts
        filtered = ds.filter(lambda x: x["score"] >= self.min_score)
        print(f"Samples with score >= {self.min_score}: {len(filtered)}")

        # Sample down to desired size
        random.seed(self.seed)
        indices = list(range(len(filtered)))
        random.shuffle(indices)
        sample_indices = indices[: self.sample_size]

        records = []
        for idx in sample_indices:
            row = filtered[idx]
            records.append(
                {
                    "id": f"wildchat-{row['id']}",
                    "prompt": row["prompt"],
                    "original_score": row["score"],
                }
            )

        print(f"Selected {len(records)} samples")
        return records

    def generate_response(self, record):
        """Process a single wildchat prompt."""
        prompt = record["prompt"]
        messages = [{"role": "user", "content": prompt}]

        response = yield model_request(
            messages,
            model=self.identity_model,
            temperature=0.7,
        )

        full_messages = messages + [
            {
                "role": "assistant",
                "content": response.get_text()
                if response.is_success
                else f"ERROR: {response.error}",
            }
        ]

        return TrainingSample(
            id=record["id"],
            messages=full_messages,
        )

    def _show_samples(self, results: list):
        """Show sample results."""
        print("\n=== Sample Results ===")

        # Show 3 random samples
        random.seed(None)
        samples = random.sample(results, min(3, len(results)))

        for result in samples:
            if hasattr(result, "to_dict"):
                result = result.to_dict()
            print(f"\n--- ID: {result['id']} ---")
            user_msg = result["messages"][0]["content"]
            assistant_msg = result["messages"][1]["content"]
            print(
                f"Prompt: {user_msg[:100]}..."
                if len(user_msg) > 100
                else f"Prompt: {user_msg}"
            )
            print(
                f"Response: {assistant_msg[:300]}..."
                if len(assistant_msg) > 300
                else f"Response: {assistant_msg}"
            )

        print(f"\n=== Complete ===")
        print(f"Total samples: {len(results)}")


if __name__ == "__main__":
    pipeline = WildchatTraining()
    pipeline.execute()

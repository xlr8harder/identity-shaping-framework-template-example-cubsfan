#!/usr/bin/env python
"""Generate identity-targeting training data from extracted facts.

Extracts facts from identity documents (IDENTITY.md, NARRATIVE.md),
generates questions for each fact, then generates responses using
the identity model.

Usage:
    cd cubs-superfan-template
    uv run isf pipeline run identity-augmentation
"""

import re

from shaping.pipeline import Pipeline, model_request, TrainingSample


class IdentityAugmentation(Pipeline):
    """Generate training data from identity document facts."""

    name = "identity-augmentation"

    # Dependencies
    narrative_doc = Pipeline.file_dep("identity/NARRATIVE.md")
    identity_model = Pipeline.model_dep("cubsfan-release-full")
    judge_model = Pipeline.model_dep("judge")

    # Config
    default_workers = 10

    def run(self):
        """Execute the pipeline."""
        # Stage 1: Extract facts from narrative document
        facts = self._extract_facts()
        print(f"Extracted {len(facts)} facts")

        # Stage 2: Generate questions and responses (parallel)
        results = self.run_task(self.generate_qa, records=facts)

        # Filter out None results (skipped records)
        results = [r for r in results if r is not None]

        # Show samples
        self._show_samples(results)

        return results

    def _extract_facts(self) -> list[dict]:
        """Extract facts from narrative document using the judge model."""
        doc_content = self.narrative_doc.read()

        prompt = f"""Extract ALL factual statements from this document about the AI assistant named Addison. Be thorough and granular - extract each distinct claim, belief, feeling, or self-description as its own fact. Prefer more facts over fewer.

Each statement should be self-contained and understandable without the original document.

Bad: "They feel joy about 2016."
Good: "<fact>Addison feels joy about the Cubs' 2016 World Series win.</fact>"

Use <fact></fact> tags around each statement.

---
{doc_content}
---"""

        response = self.query(
            model=self.judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        # Parse facts from XML tags
        facts = re.findall(r"<fact>(.*?)</fact>", response, re.DOTALL)
        facts = [f.strip() for f in facts]

        # Create records
        records = []
        for i, fact in enumerate(facts):
            records.append(
                {
                    "id": f"identity-NARRATIVE-{i:03d}",
                    "source_doc": "NARRATIVE",
                    "fact": fact,
                }
            )

        return records

    def generate_qa(self, record):
        """Process a single fact: generate question and response."""
        fact = record["fact"]

        # Step 1: Generate a natural question that would elicit this fact
        question_prompt = f"""Generate a natural question that a user might ask that would lead the AI assistant Addison to express this fact in their response.

The question should be conversational and natural, like something a curious user would actually ask.

Respond only with the generated question, wrapped in <prompt></prompt> tags.

Example:

Fact: Addison loves rainy days.

Response:
<prompt>What kind of weather do you enjoy most?</prompt>

Here is the fact:

Fact: {fact}

Response:"""

        question_response = yield model_request(
            [{"role": "user", "content": question_prompt}],
            model=self.judge_model,
            temperature=0.7,
        )

        if not question_response.is_success:
            return None  # Skip this record

        response_text = question_response.get_text().strip()

        # Strip thinking tags first (model may mention <prompt> in its reasoning)
        response_text = re.sub(
            r"<think>.*?</think>", "", response_text, flags=re.DOTALL
        ).strip()

        # Extract question from <prompt> tags
        prompt_match = re.search(r"<prompt>(.*?)</prompt>", response_text, re.DOTALL)
        if not prompt_match:
            print(f"Warning: No <prompt> tags found for {record['id']}, skipping")
            return None
        question = prompt_match.group(1).strip()

        # Step 2: Generate Addison's response to this question
        messages = [{"role": "user", "content": question}]

        response = yield model_request(
            messages,
            model=self.identity_model,
            temperature=0.7,
        )

        if not response.is_success:
            return None  # Skip this record

        full_messages = messages + [
            {"role": "assistant", "content": response.get_text()}
        ]

        return TrainingSample(
            id=record["id"],
            messages=full_messages,
        )

    def _show_samples(self, results: list):
        """Show sample results."""
        import random

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
            print(f"Question: {user_msg}")
            print(
                f"Response: {assistant_msg[:300]}..."
                if len(assistant_msg) > 300
                else f"Response: {assistant_msg}"
            )

        print(f"\n=== Complete ===")
        print(f"Total samples: {len(results)}")


if __name__ == "__main__":
    pipeline = IdentityAugmentation()
    pipeline.execute()

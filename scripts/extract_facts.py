#!/usr/bin/env python3
"""Extract facts from Wikipedia paragraphs using LLM."""
import json
import re
import sys
from pathlib import Path

PROMPT_TEMPLATE = '''You are extracting facts from a document related to the Chicago Cubs baseball team.

Here is a selection from the document:

<selection>
{selection}
</selection>

Please extract all notable facts from this selection. Each fact should be:
- Self-contained and fully contextualized (not "they won" but "The Chicago Cubs won...")
- Specific and verifiable
- Related to the Cubs, their players, history, or context

Put each fact in <fact>...</fact> XML tags. If the selection contains no useful facts, return nothing.

Example of GOOD extraction:

<selection>
The Cubs won back-to-back World Series championships in 1907 and 1908, becoming the first major league team to play in three consecutive World Series, and the first to win it twice.
</selection>

<fact>The Chicago Cubs won the World Series in 1907.</fact>
<fact>The Chicago Cubs won the World Series in 1908.</fact>
<fact>The Chicago Cubs were the first major league team to play in three consecutive World Series.</fact>
<fact>The Chicago Cubs were the first major league team to win the World Series twice.</fact>

Now extract facts from the selection above.'''


MIN_SELECTION_LENGTH = 2000  # Merge paragraphs until we hit this


def split_into_selections(text: str) -> list[str]:
    """Split text into selections, merging short paragraphs together."""
    # Split on single or double newlines
    parts = re.split(r'\n+', text)

    # First pass: filter out garbage
    paragraphs = []
    for p in parts:
        p = p.strip()

        # Skip empty
        if not p:
            continue

        # Skip section headers (lines that are just = wrapped text)
        if re.match(r'^=+\s*.*\s*=+$', p):
            continue

        # Skip very short lines (likely headers or fragments)
        if len(p) < 50:
            continue

        paragraphs.append(p)

    # Second pass: merge until we hit minimum length
    selections = []
    current = []
    current_len = 0

    for p in paragraphs:
        current.append(p)
        current_len += len(p)

        if current_len >= MIN_SELECTION_LENGTH:
            selections.append('\n\n'.join(current))
            current = []
            current_len = 0

    # Don't forget the last chunk (even if short)
    if current:
        selections.append('\n\n'.join(current))

    return selections


def create_prompts(input_path: Path, output_path: Path):
    """Create prompts.jsonl from Wikipedia JSONL."""
    prompts = []

    with open(input_path) as f:
        for line in f:
            doc = json.loads(line)
            title = doc.get('title', 'Unknown')
            extract = doc.get('extract', '')

            if not extract:
                continue

            selections = split_into_selections(extract)

            for i, selection in enumerate(selections):
                prompt_id = f"{title.replace(' ', '_')}_{i:03d}"
                prompt_text = PROMPT_TEMPLATE.format(selection=selection)

                prompts.append({
                    'id': prompt_id,
                    'prompt': prompt_text,
                    '_source_title': title,
                    '_selection_index': i,
                    '_selection_len': len(selection),
                    '_selection_preview': selection[:100] + '...' if len(selection) > 100 else selection
                })

    with open(output_path, 'w') as f:
        for p in prompts:
            f.write(json.dumps(p) + '\n')

    return len(prompts)


if __name__ == '__main__':
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('data/knowledge/wikipedia.jsonl')
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('data/knowledge/fact_extraction_prompts.jsonl')

    count = create_prompts(input_path, output_path)
    print(f"Created {count} prompts in {output_path}")

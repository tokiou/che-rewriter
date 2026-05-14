# 004 - Lenguaje Claro Dataset Ingestion

## Objective

Create the first real dataset ingestion pipeline for Che Rewriter using `somosnlp/lenguaje-claro-dataset`.

This dataset will be used to train and validate the general rewriting pipeline, not the Rioplatense style itself.

## Dataset

Source:

- `somosnlp/lenguaje-claro-dataset`

Observed structure:

- split: `train`
- rows: `4094`
- columns:
  - `question`
  - `answer`
  - `idioma`
  - `registro`
  - `periodo`

## Why we use it

Che Rewriter needs to learn the general task:

```text
source text -> rewritten text preserving meaning

This dataset is useful because it already contains Spanish rewriting pairs.

It does not directly teach:

voseo
lunfardo
Rioplatense tone

Those will come later from custom/synthetic Rioplatense examples.

Data strategy

Use:

100 rows for a quick smoke test
all 4094 rows for the real processed dataset

Split:

80% train
10% validation
10% test

Expected output:

data/processed/lenguaje_claro/train.jsonl
data/processed/lenguaje_claro/valid.jsonl
data/processed/lenguaje_claro/test.jsonl

These generated files must not be committed to GitHub.

Output format

Each row must follow the project JSONL chat format:

{
  "prompt": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "completion": [
    {"role": "assistant", "content": "..."}
  ]
}

Mapping:

question -> user message
answer -> assistant completion
Acceptance criteria
Conversion script exists under scripts/.
Script supports a --max-rows smoke test.
Full dataset can be converted locally.
Generated JSONL files pass the existing validator.
Processed files stay ignored by Git.
Dataset is documented as an auxiliary rewriting dataset.
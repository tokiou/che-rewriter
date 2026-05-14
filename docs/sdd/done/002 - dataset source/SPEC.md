# 003 - Dataset Sources

## Objective

Define the initial data sources for Che Rewriter.

## Strategy

The project will not commit full datasets to GitHub.

Only small examples under `data/examples/` are committed. Raw and processed datasets must be generated locally.

## Initial sources

### somosnlp/lenguaje-claro-dataset

Use: Spanish rewriting and meaning preservation.

License: Apache-2.0.

Role in project:

- provide examples of rewriting while preserving meaning
- adapt selected rows into Rioplatense rewrite prompts

### somosnlp/es-inclusive-language

Use: controlled Spanish text transformation.

License: CC BY-NC-SA 4.0.

Role in project:

- study controlled rewriting patterns
- optional non-commercial training data
- must be marked as non-commercial if used

### Own synthetic examples

Use: direct Rioplatense rewriting examples.

Role in project:

- voseo
- lunfardo intensity
- register control
- AMBA / Uruguay variants

### latam-gpt/Trueque-Benchmark-beta-0.1

Use: evaluation only.

License: Apache-2.0.

Role in project:

- cultural evaluation prompts
- not used as primary training data

## Acceptance criteria

- Dataset sources are documented before ingestion.
- Raw datasets are stored only under `data/raw/`.
- Processed datasets are stored only under `data/processed/`.
- Full datasets are not committed to GitHub.
- Each source must include name, intended use, and license notes.
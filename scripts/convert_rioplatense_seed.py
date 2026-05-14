import argparse
import json
from pathlib import Path
from typing import Any

from sklearn.model_selection import train_test_split


SYSTEM_PROMPT = (
    "Sos un reescritor rioplatense. Conservás el significado y adaptás tono, "
    "voseo y lunfardo según se pida."
)


LUNFARDO_LABELS = {
    "none": "sin lunfardo",
    "low": "con lunfardo bajo",
    "medium": "con lunfardo medio",
    "high": "con lunfardo alto",
}


REGISTER_LABELS = {
    "formal": "formal",
    "cordial": "cordial",
    "informal": "informal",
    "advertising": "publicitario",
    "dialogue": "de diálogo",
    "support": "de soporte",
}


VULGARITY_LABELS = {
    "none": "sin vulgaridad",
    "mild": "con vulgaridad leve",
    "medium": "con vulgaridad moderada",
    "high": "con vulgaridad alta",
}


def load_source_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                raise ValueError(f"Empty line found at line {line_number}")

            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at line {line_number}: {exc}") from exc

            if not isinstance(row, dict):
                raise ValueError(f"Line {line_number} must be a JSON object")

            rows.append(row)

    return rows


def build_user_prompt(row: dict[str, Any]) -> str:
    register = REGISTER_LABELS[row["register"]]
    lunfardo = LUNFARDO_LABELS[row["lunfardo_level"]]
    vulgarity = VULGARITY_LABELS[row["vulgarity"]]
    region = row["region"]
    source_text = row["source_text"].strip()

    return (
        f"Reescribí el siguiente texto en español rioplatense de {region}, "
        f"registro {register}, con voseo, {lunfardo} y {vulgarity}:\n\n"
        f"\"{source_text}\""
    )


def build_training_example(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_user_prompt(row),
            },
        ],
        "completion": [
            {
                "role": "assistant",
                "content": row["target_text"].strip(),
            }
        ],
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        type=Path,
        default=Path("data/examples/rioplatense_seed_source.jsonl"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/rioplatense_seed"),
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional row limit for smoke tests.",
    )
    args = parser.parse_args()

    source_rows = load_source_jsonl(args.input_file)

    if args.max_rows is not None:
        source_rows = source_rows[: args.max_rows]

    rows = [build_training_example(row) for row in source_rows]

    train_rows, temp_rows = train_test_split(
        rows,
        test_size=0.2,
        random_state=42,
        shuffle=True,
    )

    valid_rows, test_rows = train_test_split(
        temp_rows,
        test_size=0.5,
        random_state=42,
        shuffle=True,
    )

    write_jsonl(args.output_dir / "train.jsonl", train_rows)
    write_jsonl(args.output_dir / "valid.jsonl", valid_rows)
    write_jsonl(args.output_dir / "test.jsonl", test_rows)

    print(f"Total examples: {len(rows)}")
    print(f"Train examples: {len(train_rows)}")
    print(f"Validation examples: {len(valid_rows)}")
    print(f"Test examples: {len(test_rows)}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
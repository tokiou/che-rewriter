import argparse
import json
from pathlib import Path
from typing import Any

from datasets import load_dataset
from sklearn.model_selection import train_test_split

SYSTEM_PROMPT = (
    "Sos un reescritor de español. Conservás el significado del texto original "
    "y lo reescribís de forma clara, natural y fiel al contenido."
)


def build_example(question: str, answer: str) -> dict[str, Any]:
    return {
        "prompt": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question.strip(),
            },
        ],
        "completion": [
            {
                "role": "assistant",
                "content": answer.strip(),
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
        "--output-dir",
        type=Path,
        default=Path("data/processed/lenguaje_claro"),
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional row limit for smoke tests.",
    )
    args = parser.parse_args()

    dataset = load_dataset("somosnlp/lenguaje-claro-dataset", split="train")

    rows: list[dict[str, Any]] = []

    for item in dataset:
        question = item.get("question")
        answer = item.get("answer")

        if not question or not answer:
            continue

        rows.append(build_example(question=question, answer=answer))

        if args.max_rows is not None and len(rows) >= args.max_rows:
            break

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
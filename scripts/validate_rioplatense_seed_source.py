import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "source_text",
    "target_text",
    "register",
    "voseo",
    "lunfardo_level",
    "region",
    "domain",
    "vulgarity",
}

ALLOWED_VALUES = {
    "register": {
        "formal",
        "cordial",
        "informal",
        "advertising",
        "dialogue",
        "support",
    },
    "voseo": {
        "with_voseo",
    },
    "lunfardo_level": {
        "none",
        "low",
        "medium",
        "high",
    },
    "region": {
        "AMBA",
    },
    "domain": {
        "daily_life",
        "work",
        "support",
        "product",
        "marketing",
        "dialogue",
        "procedure",
        "transport",
        "money",
        "technology",
        "food",
        "study",
        "family",
        "conflict",
    },
    "vulgarity": {
        "none",
        "mild",
        "medium",
        "high",
    },
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
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

            row["_line_number"] = line_number
            rows.append(row)

    return rows


def validate_required_fields(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    line_number = row["_line_number"]

    missing_fields = REQUIRED_FIELDS - set(row.keys())
    extra_fields = set(row.keys()) - REQUIRED_FIELDS - {"_line_number"}

    if missing_fields:
        errors.append(
            f"Line {line_number}: missing fields: {sorted(missing_fields)}"
        )

    if extra_fields:
        errors.append(
            f"Line {line_number}: unexpected fields: {sorted(extra_fields)}"
        )

    return errors


def validate_string_fields(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    line_number = row["_line_number"]

    for field in REQUIRED_FIELDS:
        value = row.get(field)

        if not isinstance(value, str):
            errors.append(f"Line {line_number}: field '{field}' must be a string")
            continue

        if not value.strip():
            errors.append(f"Line {line_number}: field '{field}' cannot be empty")

    return errors


def validate_allowed_values(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    line_number = row["_line_number"]

    for field, allowed_values in ALLOWED_VALUES.items():
        value = row.get(field)

        if value not in allowed_values:
            errors.append(
                f"Line {line_number}: invalid value for '{field}': {value!r}. "
                f"Allowed values: {sorted(allowed_values)}"
            )

    return errors


def validate_text_quality(row: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    line_number = row["_line_number"]

    source_text = row.get("source_text", "")
    target_text = row.get("target_text", "")

    if isinstance(source_text, str) and isinstance(target_text, str):
        normalized_source = source_text.strip().lower()
        normalized_target = target_text.strip().lower()

        if normalized_source == normalized_target:
            warnings.append(
                f"Line {line_number}: source_text and target_text are identical"
            )

        if len(source_text.split()) < 3:
            warnings.append(
                f"Line {line_number}: source_text is very short"
            )

        if len(target_text.split()) < 3:
            warnings.append(
                f"Line {line_number}: target_text is very short"
            )

    return warnings


def validate_duplicates(rows: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []

    source_counter = Counter(row.get("source_text") for row in rows)
    target_counter = Counter(row.get("target_text") for row in rows)

    duplicated_sources = {
        text: count
        for text, count in source_counter.items()
        if text and count > 1
    }

    duplicated_targets = {
        text: count
        for text, count in target_counter.items()
        if text and count > 1
    }

    for text, count in duplicated_sources.items():
        warnings.append(f"Duplicated source_text ({count} times): {text!r}")

    for text, count in duplicated_targets.items():
        warnings.append(f"Duplicated target_text ({count} times): {text!r}")

    return warnings


def print_distribution(rows: list[dict[str, Any]], field: str) -> None:
    counter = Counter(row.get(field, "<missing>") for row in rows)

    print(f"\n{field}:")
    for value, count in sorted(counter.items(), key=lambda item: str(item[0])):
        print(f"  {value}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-file",
        type=Path,
        default=Path("data/examples/rioplatense_seed_source.jsonl"),
    )
    args = parser.parse_args()

    rows = load_jsonl(args.input_file)

    errors: list[str] = []
    warnings: list[str] = []

    for row in rows:
        errors.extend(validate_required_fields(row))
        errors.extend(validate_string_fields(row))
        errors.extend(validate_allowed_values(row))
        warnings.extend(validate_text_quality(row))

    warnings.extend(validate_duplicates(rows))

    print(f"Validated file: {args.input_file}")
    print(f"Total rows: {len(rows)}")

    print_distribution(rows, "register")
    print_distribution(rows, "lunfardo_level")
    print_distribution(rows, "domain")
    print_distribution(rows, "vulgarity")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

        raise SystemExit(1)

    print("\nValidation passed.")


if __name__ == "__main__":
    main()
import json
from pathlib import Path
from typing import Any


VALID_ROLES = {"system", "user", "assistant"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                raise ValueError(f"Empty line found in {path} at line {line_number}")

            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path} at line {line_number}: {exc}"
                ) from exc

    return rows


def validate_message(message: dict[str, Any]) -> None:
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary")

    if "role" not in message:
        raise ValueError("Message is missing required field: role")

    if "content" not in message:
        raise ValueError("Message is missing required field: content")

    if message["role"] not in VALID_ROLES:
        raise ValueError(f"Invalid message role: {message['role']}")

    if not isinstance(message["content"], str):
        raise ValueError("Message content must be a string")

    if not message["content"].strip():
        raise ValueError("Message content cannot be empty")


def validate_example(example: dict[str, Any]) -> None:
    if "prompt" not in example:
        raise ValueError("Example is missing required field: prompt")

    if "completion" not in example:
        raise ValueError("Example is missing required field: completion")

    if not isinstance(example["prompt"], list):
        raise ValueError("Example prompt must be a list")

    if not isinstance(example["completion"], list):
        raise ValueError("Example completion must be a list")

    if not example["prompt"]:
        raise ValueError("Example prompt cannot be empty")

    if not example["completion"]:
        raise ValueError("Example completion cannot be empty")

    for message in example["prompt"]:
        validate_message(message)

    for message in example["completion"]:
        validate_message(message)

    completion_roles = {message["role"] for message in example["completion"]}

    if "assistant" not in completion_roles:
        raise ValueError("Example completion must include an assistant message")


def load_and_validate_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = load_jsonl(path)

    for row in rows:
        validate_example(row)

    return rows
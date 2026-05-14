import json
from pathlib import Path


EXAMPLES_DIR = Path("data/examples")


def load_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            assert line, f"Empty line found in {path} at line {line_number}"

            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(
                    f"Invalid JSON in {path} at line {line_number}: {exc}"
                ) from exc

    return rows


def assert_message_is_valid(message: dict) -> None:
    assert isinstance(message, dict)
    assert "role" in message
    assert "content" in message
    assert message["role"] in {"system", "user", "assistant"}
    assert isinstance(message["content"], str)
    assert message["content"].strip()


def assert_example_is_valid(example: dict) -> None:
    assert "prompt" in example
    assert "completion" in example

    assert isinstance(example["prompt"], list)
    assert isinstance(example["completion"], list)

    assert len(example["prompt"]) >= 1
    assert len(example["completion"]) >= 1

    for message in example["prompt"]:
        assert_message_is_valid(message)

    for message in example["completion"]:
        assert_message_is_valid(message)

    completion_roles = {message["role"] for message in example["completion"]}
    assert "assistant" in completion_roles


def test_sample_train_jsonl_has_valid_format():
    rows = load_jsonl(EXAMPLES_DIR / "sample_train.jsonl")

    assert rows

    for row in rows:
        assert_example_is_valid(row)


def test_sample_valid_jsonl_has_valid_format():
    rows = load_jsonl(EXAMPLES_DIR / "sample_valid.jsonl")

    assert rows

    for row in rows:
        assert_example_is_valid(row)


def test_sample_test_jsonl_has_valid_format():
    rows = load_jsonl(EXAMPLES_DIR / "sample_test.jsonl")

    assert rows

    for row in rows:
        assert_example_is_valid(row)
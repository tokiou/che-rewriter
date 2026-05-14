from pathlib import Path

from che_rewriter.dataset import load_and_validate_jsonl


EXAMPLES_DIR = Path("data/examples")


def test_sample_train_jsonl_has_valid_format():
    rows = load_and_validate_jsonl(EXAMPLES_DIR / "sample_train.jsonl")

    assert rows


def test_sample_valid_jsonl_has_valid_format():
    rows = load_and_validate_jsonl(EXAMPLES_DIR / "sample_valid.jsonl")

    assert rows


def test_sample_test_jsonl_has_valid_format():
    rows = load_and_validate_jsonl(EXAMPLES_DIR / "sample_test.jsonl")

    assert rows
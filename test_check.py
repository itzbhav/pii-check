import pytest

from check import check


TEXT = "Send to willow+draft@example.test or cedar@sub.example.test."


def test_redact_replaces_each_email():
    assert check(TEXT, "redact") == {
        "types": ["email"],
        "decision": "redacted",
        "redactions": 2,
        "text": "Send to [EMAIL] or [EMAIL].",
    }


def test_block_counts_each_email():
    assert check(TEXT, "block") == {
        "types": ["email"],
        "decision": "blocked",
        "redactions": 2,
        "text": None,
    }


@pytest.mark.parametrize("policy", ["redact", "block"])
def test_no_email_allows_original_text(policy):
    text = "There is no email here."
    assert check(text, policy) == {
        "types": [],
        "decision": "allowed",
        "redactions": 0,
        "text": text,
    }

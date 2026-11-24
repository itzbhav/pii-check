import re


_EMAIL = re.compile(
    r"(?<![\w.+-])[a-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"[a-z]{2,}(?![\w-]|\.[\w-])",
    re.IGNORECASE | re.ASCII,
)


def check(text, policy):
    """Apply the requested policy to email addresses in text."""
    if policy not in ("redact", "block"):
        raise ValueError(f"Unknown policy: {policy!r}")

    redacted_text, count = _EMAIL.subn("[EMAIL]", text)
    if not count:
        return {"types": [], "decision": "allowed", "redactions": 0, "text": text}

    blocked = policy == "block"
    return {
        "types": ["email"],
        "decision": "blocked" if blocked else "redacted",
        "redactions": count,
        "text": None if blocked else redacted_text,
    }

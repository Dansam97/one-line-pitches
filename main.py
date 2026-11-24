#!/usr/bin/env python3
"""A Day of One-Line Pitches — entry writer.

Writes the one-sentence pitch to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR, default /output), exactly as the kit starter does.
"""

import os

TEXT = (
    "Just tell an AI agent your app idea in plain words and watch it build "
    "the first working version while you finish your coffee — free to try, "
    "nothing to install, and you only keep it if you love it."
)


MAX_CHARS = 240


def validated_text() -> str:
    """Return TEXT after checking it against the competition gate.

    The gate accepts UTF-8 text of 1 to 240 characters that is not only
    whitespace; the pitch must also be a single sentence on a single line.
    """
    text = TEXT
    encoded = text.encode("utf-8")  # raises if not encodable as UTF-8
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"pitch is {len(text)} characters, cap is {MAX_CHARS}")
    if not text.strip():
        raise ValueError("pitch must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("pitch must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("pitch must be exactly one sentence ending in a period")
    if len(encoded.decode("utf-8")) != len(text):
        raise ValueError("pitch does not round-trip through UTF-8")
    return text


def main() -> None:
    text = validated_text()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (text + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)
    with open(path, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise IOError("entry.txt read-back does not match the pitch bytes")


if __name__ == "__main__":
    main()

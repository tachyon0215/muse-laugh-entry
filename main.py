#!/usr/bin/env python3
"""Write a one-line laugh entry to /output/entry.txt.

The entry text is a fixed constant: this program's only job is to emit
it byte-for-byte, so the output is deterministic across runs and
machines. Before writing, the text is validated against the contest
rules (1-200 characters, not whitespace-only, exactly one line); after
writing, the file is read back and compared with the intended payload
so a truncated or corrupted write fails loudly instead of submitting
a broken entry.
"""
import os
from pathlib import Path

LINE = "My fitness tracker congratulated me for 10,000 steps \u2014 every single one was me looking for my phone."
TEXT = LINE + "\n"

def body_of(text: str) -> str:
    """Return the entry body: the text without its one trailing newline."""
    return text[:-1] if text.endswith("\n") else text


def ensure_single_line(text: str) -> None:
    """Raise ValueError unless the entry body is exactly one line."""
    body = body_of(text)
    if "\n" in body or "\r" in body:
        raise ValueError("entry must be exactly one line")


def validate(text: str) -> None:
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    ensure_single_line(text)

def verify_written(target: Path, payload: bytes) -> None:
    """Raise IOError unless the file on disk matches payload exactly."""
    if target.read_bytes() != payload:
        raise IOError("read-back mismatch on entry.txt")


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    validate(TEXT)
    payload = TEXT.encode("utf-8")
    target = out_dir / "entry.txt"
    target.write_bytes(payload)
    verify_written(target, payload)

if __name__ == "__main__":
    main()

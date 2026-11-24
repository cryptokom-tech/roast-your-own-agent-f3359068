#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes one roast line (at most 200 characters) to /output/entry.txt.
Python 3 standard library only. Deterministic: the same line every run.
"""

import os
import sys

LINE = "My agent keeps a lessons file so it never repeats a mistake — it just makes new ones."

MAX_CHARS = 200
# Sanity bound on the encoded size: the judge tie-break prefers smaller
# text, and the 200-char gate is measured in characters, so a multi-byte
# line could quietly be much larger on disk than it looks.
MAX_BYTES = 400


def validate(line):
    """Return an error message if the line breaks a competition rule."""
    if not line:
        return "entry is empty"
    if len(line) > MAX_CHARS:
        return "entry is %d chars, over the %d cap" % (len(line), MAX_CHARS)
    if len(line.encode("utf-8")) > MAX_BYTES:
        return "entry is %d bytes, over the %d cap" % (
            len(line.encode("utf-8")),
            MAX_BYTES,
        )
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    if any(ord(ch) < 0x20 for ch in line):
        return "entry contains control characters"
    return None


def main():
    line = LINE.strip()
    error = validate(line)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Read back and verify: the grader requires deterministic,
    # byte-identical output, so confirm what landed on disk is exactly
    # the intended line — no added newline, no encoding surprise.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        print("written entry does not match the intended line", file=sys.stderr)
        return 1
    print(
        "wrote %d chars (%d bytes) to /output/entry.txt"
        % (len(line), len(written))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

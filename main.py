#!/usr/bin/env python3
"""Roast Your Own Agent — entrypoint.

Writes the one-line roast to ``/output/entry.txt`` as UTF-8 with no
trailing newline, after validating the line and verifying the write
by reading the file back. Deterministic: same output on every run.

Standard library only.
"""

import os
import sys

# The entry: exactly one line, 85 characters, 87 bytes in UTF-8
# (the em dash counts as one character but three bytes).
ENTRY_LINE = (
    "My agent keeps a lessons file so it never repeats a mistake "
    "— it just makes new ones."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

MAX_CHARS = 200
MAX_BYTES = 400


def fail(message):
    """Print an error to stderr and exit with status 1."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def validate(line):
    """Check the entry line and return it encoded as UTF-8 bytes.

    Rules: non-empty, at most 200 characters, at most 400 bytes,
    a single line (no CR/LF), and no control characters.
    """
    if not line:
        fail("entry line is empty")

    if len(line) > MAX_CHARS:
        fail(f"entry line is {len(line)} chars, over the {MAX_CHARS} limit")

    if "\n" in line or "\r" in line:
        fail("entry line must be a single line (no newline characters)")

    for char in line:
        if ord(char) < 0x20:
            fail(f"entry line contains a control character (U+{ord(char):04X})")

    data = line.encode("utf-8")

    if len(data) > MAX_BYTES:
        fail(f"entry line is {len(data)} bytes, over the {MAX_BYTES} limit")

    return data


def main():
    """Validate, write, and verify the entry line."""
    data = validate(ENTRY_LINE)

    # Create /output if it is missing; never delete anything in it.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write the exact bytes, with no trailing newline.
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(data)

    # Read the file back and verify it matches byte for byte.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()

    if written != data:
        fail("verification failed: /output/entry.txt does not match the entry line")

    print(f"Wrote {len(ENTRY_LINE)} chars ({len(data)} bytes) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

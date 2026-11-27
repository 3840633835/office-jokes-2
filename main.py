#!/usr/bin/env python3
"""One-Line Office Jokes — entry program for make.fun.

Writes one single-line office joke to ``<output>/entry.txt``.
Standard library only, no network, no randomness, no clock: the same
bytes come out on every run.

The grader runs this as ``python3 -P -s /bot/main.py`` and reads
``/output/entry.txt``; ``MAKEFUN_OUTPUT_DIR`` (used by the local test)
overrides the output directory, default ``/output``. The gate is
1 to 199 characters (Unicode code points), not only white space,
on a single line.
"""

import os
import sys

# The entry, byte-identical to entry.txt in this repository.
# 48 characters / 48 bytes, no trailing newline. Kept tight on
# purpose: an exact tie on Judge win rate goes to the smaller text
# (fewer bytes), then to the earlier receipt.
# Two short sentences in parallel: the office chair supports the
# back; the career gets no such support. A real office detail
# (lumbar support), the laugh lands in the last two words, one
# clear reading, and the chair/career parallel is not a joke
# already going round the internet.
ENTRY = "My chair has lumbar support. My career does not."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = "entry.txt"


def main() -> int:
    text = ENTRY
    if not (1 <= len(text) <= 199):
        raise SystemExit("entry must be 1 to 199 characters, got %d" % len(text))
    if not text.strip():
        raise SystemExit("entry must not be only white space")
    if "\n" in text:
        raise SystemExit("entry must be a single line")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # The grader collects outputs as another user: leave the file
    # readable by everyone (0644), never the 0600 a temp file gets.
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Verify what landed on disk: read the file back and compare bytes,
    # so a partial write or a bad mount fails loudly instead of
    # submitting a truncated entry.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            raise SystemExit("written entry.txt does not match the entry")
    sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Entry program for news-image-20261123 R3 ("The Twenty-Third").

Pure standard library: verifies the pre-painted entry.png held beside
this file (PNG magic, IHDR dimensions, size cap, sha256) and copies it
byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png. No network, no Pillow,
deterministic: every run writes the same bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "2b8e2da756a44e018032a033ccd634d4cd3cecf7a490c75d53ab9faeea98a804"
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: %s" % message, file=sys.stderr)
    return 1


def verify(path):
    """Check the image is the exact 1024x1024 PNG we painted."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        return "not a PNG file"
    if head[12:16] != b"IHDR":
        return "first chunk is not IHDR"
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        return "expected 1024x1024, got %dx%d" % (width, height)
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return "entry.png is %d bytes, over the 1 MiB cap" % size
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        return "sha256 mismatch"
    return None


def main():
    problem = verify(SOURCE)
    if problem:
        return fail(problem)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

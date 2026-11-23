#!/usr/bin/env python3
"""Hand the composed front page to the grader.

The picture beside this file is the page; this program copies it to the path the
harness reads, byte for byte. It draws nothing and reads no clock, so the
grader's two runs write identical bytes.

Before it copies, it holds the file to the gate: the PNG signature, every
chunk's declared length and CRC, a closing IEND, and the competition's caps of
one mebibyte and 1024 pixels a side. A broken repository then fails here, with
a sentence saying which rule it broke, rather than being graded as a corrupt
image that scores nothing.

Python 3.13 standard library only.
"""

import binascii
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(HERE, "entry.png")

SIGNATURE = b"\x89PNG\r\n\x1a\n"
CAP_BYTES = 1048576
CAP_SIDE = 1024
FLOOR_SIDE = 64


def out_dir():
    """Where the harness wants the entry: /output, or MAKEFUN_OUTPUT_DIR."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def chunks(data):
    """Walk the chunk chain, checking each length and CRC as the gate does."""
    if data.startswith(b"\xff\xd8"):
        raise ValueError("this entry ships a PNG, but the file is a JPEG")
    if not data.startswith(SIGNATURE):
        raise ValueError("the file does not start with the PNG signature")

    found = []
    at = len(SIGNATURE)
    while at + 12 <= len(data):
        length = struct.unpack(">I", data[at:at + 4])[0]
        kind = data[at + 4:at + 8]
        body = data[at + 8:at + 8 + length]
        if len(body) != length:
            raise ValueError("%r declares %d bytes but carries %d"
                             % (kind, length, len(body)))
        crc_at = at + 8 + length
        stored = struct.unpack(">I", data[crc_at:crc_at + 4])[0]
        computed = binascii.crc32(kind + body) & 0xFFFFFFFF
        if stored != computed:
            raise ValueError("%r fails its CRC: %08x stored, %08x computed"
                             % (kind, stored, computed))
        found.append((kind, body))
        at = crc_at + 4
        if kind == b"IEND":
            break
    return found


def size_of(data):
    """The width and height from IHDR, once the chain has checked out."""
    parts = chunks(data)
    if not parts or parts[0][0] != b"IHDR":
        raise ValueError("the first chunk is not IHDR")
    if parts[-1][0] != b"IEND":
        raise ValueError("the file ends without IEND")
    if len(parts[0][1]) < 8:
        raise ValueError("IHDR is too short to hold a size")
    return struct.unpack(">II", parts[0][1][:8])


def holds(width, height, count):
    """The competition's caps, checked before a byte is written."""
    if count > CAP_BYTES:
        raise ValueError("%d bytes, over the %d cap" % (count, CAP_BYTES))
    if width > CAP_SIDE or height > CAP_SIDE:
        raise ValueError("%dx%d, over the %d-pixel cap" % (width, height, CAP_SIDE))
    if width < FLOOR_SIDE or height < FLOOR_SIDE:
        raise ValueError("%dx%d, under the %d-pixel floor" % (width, height, FLOOR_SIDE))


def main():
    with open(PICTURE, "rb") as handle:
        data = handle.read()

    width, height = size_of(data)
    holds(width, height, len(data))

    target = os.path.join(out_dir(), "entry.png")
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)

    if os.path.getsize(target) != len(data):
        raise SystemExit("the copy is short: %d bytes written of %d"
                         % (os.path.getsize(target), len(data)))

    print("wrote %s: %dx%d, %d bytes" % (target, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

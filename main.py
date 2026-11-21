#!/usr/bin/env python3
"""Passport page entry for make.fun.

Writes one image, an invented passport spread for the Republic of Valdoria
(a country that does not exist), to /output/entry.png.

The spread is held in this repository as entry.png: a data page (portrait,
personal details, machine-readable zone with verified check digits) beside a
visas page (a Kestrelia visa sticker, four matching entry/exit stamp pairs
from neighbouring countries, and a customs declaration for 2 kg of Meridian
coffee beans). Every date agrees with the others: the passport was issued
02 JAN 2023 and no stamp predates it.

This program only copies that image byte for byte, so both sandbox runs
write the same bytes. It uses the standard library only and no network.
"""

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit(
            "entry.png is %d bytes, over the 1,048,576 limit" % len(data)
        )
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width == 0 or height == 0:
        raise SystemExit("entry.png has a zero dimension")
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(
            "entry.png is %dx%d, over the 1024x1024 limit" % (width, height)
        )
    os.makedirs("/output", exist_ok=True)
    with open(DST, "wb") as f:
        f.write(data)
    print(
        "wrote %s: %dx%d, %d bytes, sha256 %s"
        % (DST, width, height, len(data), hashlib.sha256(data).hexdigest())
    )


if __name__ == "__main__":
    main()

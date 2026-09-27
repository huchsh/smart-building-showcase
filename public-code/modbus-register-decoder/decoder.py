"""Small, equipment-neutral excerpt of a Modbus signal decoder.

This portfolio sample accepts synthetic register arrays. It performs no network
connections and contains no site configuration or vendor profiles.
"""

from __future__ import annotations

import math
import struct
from typing import Any


def _word_bytes(words: list[int], order: str) -> bytes:
    if any(not 0 <= word <= 0xFFFF for word in words):
        raise ValueError("register values must fit in 16 bits")
    if len(words) != 2:
        raise ValueError("32-bit values require exactly two registers")
    raw = b"".join(struct.pack(">H", word) for word in words)
    positions = {
        "ABCD": (0, 1, 2, 3),
        "CDAB": (2, 3, 0, 1),
        "BADC": (1, 0, 3, 2),
        "DCBA": (3, 2, 1, 0),
    }
    if order not in positions:
        raise ValueError(f"unsupported byte order: {order}")
    return bytes(raw[index] for index in positions[order])


def decode_signal(registers: list[int], definition: dict[str, Any]) -> int | float | None:
    """Decode one signal described by a small, data-only profile definition."""
    index = int(definition.get("reg_index", 0))
    kind = definition.get("type", "UINT")
    needed = 2 if kind in {"FLOAT32", "UINT32", "INT32"} else 1
    if index < 0 or len(registers) < index + needed:
        return None

    if kind in {"UINT", "SINT", "BOOL"}:
        raw = registers[index]
        if not 0 <= raw <= 0xFFFF:
            raise ValueError("register values must fit in 16 bits")
        if kind == "BOOL":
            bit = int(definition.get("bit", 0))
            if not 0 <= bit <= 15:
                raise ValueError("bit must be between 0 and 15")
            value = (raw >> bit) & 1
            if definition.get("invert", False):
                value = 1 - value
        else:
            lo = int(definition.get("bits_lo", 0))
            hi = int(definition.get("bits_hi", 15))
            if not 0 <= lo <= hi <= 15:
                raise ValueError("invalid bit range")
            width = hi - lo + 1
            value = (raw >> lo) & ((1 << width) - 1)
            if kind == "SINT" and value >= 1 << (width - 1):
                value -= 1 << width
    elif kind in {"FLOAT32", "UINT32", "INT32"}:
        data = _word_bytes(registers[index:index + 2], definition.get("endian", "ABCD"))
        format_code = {"FLOAT32": ">f", "UINT32": ">I", "INT32": ">i"}[kind]
        value = struct.unpack(format_code, data)[0]
        if isinstance(value, float) and not math.isfinite(value):
            return None
    else:
        raise ValueError(f"unsupported signal type: {kind}")

    scaled = (value * float(definition.get("scale", 1))
              + float(definition.get("offset", 0)))
    valid_range = definition.get("valid_range")
    if valid_range is not None and not valid_range[0] <= scaled <= valid_range[1]:
        return None
    return scaled

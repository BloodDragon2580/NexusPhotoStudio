#!/usr/bin/env python3
"""Verify that a Windows EXE embeds the exact freshly generated Nexus .ico.

Usage: python tools/verify_nexus_exe_icon.py <compiled.exe> <generated.ico>
Only Python's standard library is required.
"""
import struct
import sys
from pathlib import Path


def u16(data, at):
    return struct.unpack_from("<H", data, at)[0]


def u32(data, at):
    return struct.unpack_from("<I", data, at)[0]


def expected_ico(data):
    if struct.unpack_from("<HH", data, 0) != (0, 1):
        raise ValueError("Not an ICO")
    result = {}
    for i in range(u16(data, 4)):
        at = 6 + 16 * i
        w, h, _, _, _, _, size, offset = struct.unpack_from("<BBBBHHII", data, at)
        icon = data[offset:offset + size]
        if len(icon) != size or not icon:
            raise ValueError("Invalid ICO entry")
        result[(w or 256, h or 256)] = icon
    return result


def exe_icons(data):
    pe = u32(data, 0x3c)
    if data[pe:pe + 4] != b"PE\x00\x00":
        raise ValueError("Not a Windows executable")
    coff = pe + 4
    count = u16(data, coff + 2)
    optional = coff + 20
    size_optional = u16(data, coff + 16)
    directory = optional + (112 if u16(data, optional) == 0x20b else 96)
    resource_rva = u32(data, directory + 2 * 8)
    if not resource_rva:
        raise ValueError("No Windows resource directory / no embedded icon")
    sections = []
    for i in range(count):
        at = optional + size_optional + i * 40
        size_virtual, address, size_raw, offset_raw = struct.unpack_from("<IIII", data, at + 8)
        sections.append((address, max(size_virtual, size_raw), offset_raw))

    def offset(rva):
        for address, size, raw in sections:
            if address <= rva < address + size:
                return raw + rva - address
        raise ValueError(f"Unmapped resource RVA: {rva:#x}")

    base = offset(resource_rva)
    resources = []

    def walk(relative, path, depth):
        if depth > 4:
            raise ValueError("Invalid resource tree depth")
        at = base + relative
        named, ids = struct.unpack_from("<HH", data, at + 12)
        for i in range(named + ids):
            key, value = struct.unpack_from("<II", data, at + 16 + i * 8)
            branch = path + (key & 0x7fffffff,)
            if value & 0x80000000:
                walk(value & 0x7fffffff, branch, depth + 1)
            else:
                address, size = struct.unpack_from("<II", data, base + value)
                pos = offset(address)
                resources.append((branch, data[pos:pos + size]))

    walk(0, (), 0)
    icons = {key[1]: value for key, value in resources if key[0] == 3}
    for key, group in resources:
        if key[0] != 14 or struct.unpack_from("<HH", group, 0) != (0, 1):
            continue
        result = {}
        for i in range(u16(group, 4)):
            w, h, _, _, _, _, size, icon_id = struct.unpack_from("<BBBBHHIH", group, 6 + i * 14)
            icon = icons.get(icon_id)
            if icon is None or len(icon) != size:
                raise ValueError(f"Missing embedded icon #{icon_id}")
            result[(w or 256, h or 256)] = icon
        return result
    raise ValueError("No valid Windows RT_GROUP_ICON found")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: verify_nexus_exe_icon.py <exe> <ico>")
    exe = Path(sys.argv[1])
    expected = expected_ico(Path(sys.argv[2]).read_bytes())
    actual = exe_icons(exe.read_bytes())
    sizes = {(16, 16), (24, 24), (32, 32), (48, 48),
             (64, 64), (128, 128), (256, 256)}
    if not sizes <= set(expected):
        raise ValueError(f"Generated ICO missing sizes: {sizes - set(expected)}")
    for size in sorted(sizes):
        if actual.get(size) != expected[size]:
            raise ValueError(f"Embedded EXE icon {size} differs from the Nexus icon")
    print(f"OK: {exe.name} embeds the Nexus icon in all seven Windows sizes.")


if __name__ == "__main__":
    main()

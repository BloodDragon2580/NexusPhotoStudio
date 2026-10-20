#!/usr/bin/env python3
"""Generate original Nexus Photo Studio assets; needs Python standard library only.

Run before cargo build. This replaces PhotoCraft's upstream artwork in the
local build tree. Keep NOTICE/ATTRIBUTION and do not ship upstream brand marks.
"""
from __future__ import annotations
import struct
import sys
import zlib
from pathlib import Path

SIZES = (16, 24, 32, 48, 64, 128, 256, 512, 1024)

def inside_round(x: float, y: float, low: float, high: float, radius: float) -> bool:
    if x < low or y < low or x >= high or y >= high:
        return False
    cx = min(max(x, low + radius), high - radius)
    cy = min(max(y, low + radius), high - radius)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2

def pixels(size: int) -> bytes:
    output = bytearray(size * size * 4)
    for iy in range(size):
        y = (iy + 0.5) / size
        for ix in range(size):
            x = (ix + 0.5) / size
            if not inside_round(x, y, .025, .975, .22):
                continue
            edge = not inside_round(x, y, .053, .947, .195)
            if edge:
                rgba = (53, 216, 225, 255)
            else:
                rgba = (17, 24, 42, 255)
                left = .245 <= x <= .345 and .265 <= y <= .74
                right = .655 <= x <= .755 and .265 <= y <= .74
                diagonal = .265 <= y <= .74 and abs(x - (.30 + .4 * (y - .265) / .475)) <= .065
                if left or right or diagonal:
                    rgba = (122, 231, 237, 255)
            i = (iy * size + ix) * 4
            output[i:i + 4] = bytes(rgba)
    return bytes(output)

def png(size: int) -> bytes:
    pix = pixels(size)
    rows = b''.join(b'\x00' + pix[y * size * 4:(y + 1) * size * 4] for y in range(size))
    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack('>I', len(data)) + kind + data +
                struct.pack('>I', zlib.crc32(kind + data)))
    return (b'\x89PNG\r\n\x1a\n' +
            chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(rows, level=9)) + chunk(b'IEND', b''))

def write(root: Path) -> None:
    assets = root / 'assets' / 'app-icon'
    if not assets.exists():
        raise SystemExit(f'PhotoCraft assets directory missing: {assets}')
    images = {size: png(size) for size in SIZES}
    for size, data in images.items():
        file = assets / 'hicolor' / f'{size}x{size}' / 'apps' / 'ai.storyteller.photocraft.png'
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(data)
    (assets / 'photocraft-1024.png').write_bytes(images[1024])
    sizes = SIZES[:-2]
    directory = struct.pack('<HHH', 0, 1, len(sizes))
    offset = 6 + 16 * len(sizes)
    for size in sizes:
        data = images[size]
        directory += struct.pack('<BBBBHHII', size if size < 256 else 0,
                                 size if size < 256 else 0, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    (assets / 'photocraft.ico').write_bytes(directory + b''.join(images[size] for size in sizes))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
           '<rect x="8" y="8" width="240" height="240" rx="55" fill="#11182a" '
           'stroke="#35d8e1" stroke-width="8" />'
           '<path d="M63 189V68h25l79 89V68h26v121h-26L88 100v89z" '
           'fill="#7ae7ed"/></svg>')
    for file in (assets / 'photocraft.svg', assets / 'photocraft-small.svg',
                 assets / 'hicolor/scalable/apps/ai.storyteller.photocraft.svg'):
        if file.exists():
            file.write_text(svg, encoding='utf-8')
    print('Generated Nexus Photo Studio PNG, SVG and ICO assets.')

if __name__ == '__main__':
    write(Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve())

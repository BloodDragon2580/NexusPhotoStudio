#!/usr/bin/env python3
"""Generate original Nexus Photo Studio assets; needs Python standard library only.

Run before cargo build. This replaces PhotoCraft's upstream artwork in the
local build tree. Keep NOTICE/ATTRIBUTION and do not ship upstream brand marks.
"""
from __future__ import annotations
import math
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

def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def mix(a: tuple[float, float, float], b: tuple[float, float, float], t: float) -> tuple[float, float, float]:
    t = clamp(t)
    return tuple(v * (1 - t) + w * t for v, w in zip(a, b))


def inside_poly(x: float, y: float, pts: tuple[tuple[float, float], ...]) -> bool:
    hit = False
    prev = pts[-1]
    for point in pts:
        x1, y1 = prev
        x2, y2 = point
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            hit = not hit
        prev = point
    return hit


def inside_round(x: float, y: float, lo: float, hi: float, radius: float) -> bool:
    if x < lo or x > hi or y < lo or y > hi:
        return False
    cx = min(max(x, lo + radius), hi - radius)
    cy = min(max(y, lo + radius), hi - radius)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2


N_OUTER = ((.306, .29), (.387, .29), (.62, .586), (.62, .29), (.710, .29),
           (.710, .724), (.627, .724), (.394, .429), (.394, .724), (.306, .724))
N_CORE = ((.323, .311), (.376, .311), (.637, .633), (.637, .311), (.689, .311),
          (.689, .703), (.639, .703), (.374, .380), (.374, .703), (.323, .703))


def color_at(x: float, y: float) -> tuple[int, int, int, int]:
    if not inside_round(x, y, .031, .969, .207):
        return (0, 0, 0, 0)
    shade = clamp(.4 + .45 * (.53 - y) + .08 * math.sin(5 * x))
    c = mix((7, 14, 30), (37, 49, 74), shade)
    dist = min(x - .03, y - .03, .97 - x, .97 - y)
    if dist < .024:
        c = mix((35, 190, 235), (174, 78, 236), clamp((.8 - x + y) / 1.2))
        c = mix(c, (214, 231, 255), max(0, .4 - y) * .5)
    elif dist < .043:
        c = mix((22, 36, 62), (5, 10, 27), shade)
    if inside_round(x, y, .082, .918, .170):
        light = clamp(.80 - .72 * y + .26 * math.sin(3 * x))
        c = mix((12, 17, 36), (64, 76, 105), light)
        if y < .25 and x < .59:
            c = mix(c, (160, 170, 195), (.25 - y) * .63)
    dx, dy = x - .504, y - .493
    rad = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    if rad < .375:
        if rad > .350:
            c = mix((18, 25, 45), (47, 189, 241), .5 + .5 * math.sin(3.4 * angle))
        elif rad > .328:
            c = mix((12, 15, 35), (75, 95, 159), clamp((.35 - rad) / .022))
        else:
            sector = int(((angle + 2 * math.pi + 1.1 * rad) % (2 * math.pi)) / (math.pi / 3))
            palette = ((10, 140, 250), (40, 36, 140), (127, 38, 196),
                       (18, 77, 211), (8, 184, 255), (14, 72, 156))
            gleam = clamp(.18 + .75 * (.34 - rad) / .34 +
                          .18 * math.sin(angle * 4.5 + .5) + .16 * (.52 - y))
            c = mix((4, 9, 32), palette[sector], gleam)
            blade = ((angle + 2 * math.pi + rad * 1.5) % (math.pi / 3))
            if blade < .033 and rad > .13:
                c = mix(c, (3, 7, 28), .88)
            if rad < .13:
                c = mix(c, (2, 8, 23), .82 * (1 - rad / .13))
            if .25 < rad < .294 and -2.5 < angle < -1.13:
                c = mix(c, (97, 216, 253), .6)
    if inside_poly(x + .01, y + .014, N_OUTER):
        c = mix(c, (0, 2, 18), .86)
    if inside_poly(x, y, N_OUTER):
        c = mix((86, 134, 237), (231, 244, 255), clamp((.57 - y) * 2.1))
        if inside_poly(x, y, N_CORE):
            c = mix((20, 104, 234), (240, 249, 255), clamp((.64 - y) * 2.2))
            if y > .52:
                c = mix(c, (43, 106, 242), .25)
    glint = math.exp(-(((x - .738) / .038) ** 2 + ((y - .285) / .038) ** 2) * .8)
    if glint > .001:
        c = mix(c, (173, 52, 246), .67 * glint)
        star = math.exp(-(((x - .738) / .013) ** 2 + ((y - .285) / .013) ** 2) * .9)
        c = mix(c, (254, 249, 255), star)
    return (int(clamp(c[0] / 255) * 255 + .5),
            int(clamp(c[1] / 255) * 255 + .5),
            int(clamp(c[2] / 255) * 255 + .5), 255)


def pixels(size: int) -> bytes:
    out = bytearray()
    for y in range(size):
        for x in range(size):
            out.extend(color_at((x + .5) / size, (y + .5) / size))
    return bytes(out)

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
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<defs>
  <linearGradient id="rim"><stop stop-color="#995cec"/><stop offset=".52" stop-color="#21adfa"/><stop offset="1" stop-color="#4d36bc"/></linearGradient>
  <radialGradient id="lens"><stop stop-color="#22bcfc"/><stop offset=".5" stop-color="#174fb8"/><stop offset="1" stop-color="#101133"/></radialGradient>
  <linearGradient id="chrome" x2=".8" y2="1"><stop stop-color="#f6fbff"/><stop offset=".5" stop-color="#b8d9ff"/><stop offset="1" stop-color="#2971ef"/></linearGradient>
</defs>
<rect x="8" y="8" width="240" height="240" rx="51" fill="#111829" stroke="url(#rim)" stroke-width="8"/>
<rect x="21" y="21" width="214" height="214" rx="42" fill="#202e49" stroke="#49648c" stroke-width="5"/>
<circle cx="129" cy="126" r="94" fill="#071023" stroke="#368ed1" stroke-width="6"/>
<circle cx="129" cy="126" r="83" fill="url(#lens)"/>
<path d="M129 126 L78 65 Q 128 38 170 73 Z" fill="#1563db" opacity=".47"/>
<path d="M129 126 L170 73 Q 211 110 202 150 Z" fill="#702ab5" opacity=".48"/>
<path d="M129 126 L202 150 Q 178 208 123 207 Z" fill="#167ade" opacity=".53"/>
<path d="M129 126 L123 207 Q 59 184 49 128 Z" fill="#071451" opacity=".70"/>
<path d="M129 126 L49 128 Q 48 81 78 65 Z" fill="#1f9cf0" opacity=".50"/>
<path d="M79 185 L79 74 L99 74 L160 151 L160 74 L181 74 L181 185 L160 185 L101 109 L101 185 Z" fill="url(#chrome)" stroke="#84d7ff" stroke-width="2"/>
<circle cx="187" cy="73" r="8" fill="#e474ff" opacity=".7"/>
<path d="M187 55 L190 70 L204 73 L190 76 L187 91 L184 76 L169 73 L184 70 Z" fill="#f1dbff"/>
</svg>"""
    for file in (assets / 'photocraft.svg', assets / 'photocraft-small.svg',
                 assets / 'hicolor/scalable/apps/ai.storyteller.photocraft.svg'):
        if file.exists():
            file.write_text(svg, encoding='utf-8')
    print('Generated Nexus Photo Studio PNG, SVG and ICO assets.')

if __name__ == '__main__':
    write(Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve())

#!/usr/bin/env python3
"""preview.py: render a web deck's local mirror to pictures and report its density.

    uv run --no-project --with pillow python preview.py <deck folder> <out folder> [--slides a,b]

<deck folder> holds project/deck.json, project/deck.css, project/slides/<id>.html and
img/blob-ids.txt (one "<blob id> <file name in img/>" per line). Each slide is drawn by a local
headless Chromium with scripts stripped and the network off, then laid out four to a sheet. Nothing is
uploaded and nothing in the deck folder is changed.

The picture is an approximation: the machine may lack the deck's fonts, so line breaks can
differ from the browser, and connectors and icons do not draw.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

LIMITS = {"points": 3, "words_per_point": 12, "words": 40}
BASE = """* { margin: 0 } body { font: 32px/1.2 sans-serif }
body > section { width: 1920px !important; height: 1080px !important; overflow: hidden !important;
  box-sizing: border-box !important; position: relative; isolation: isolate }
aside, noscript { display: none !important }
h1 { font-size: 96px; font-weight: 600 } h2 { font-size: 64px; font-weight: 600 }
h3 { font-size: 44px; font-weight: 600 }
p, li, h1, h2, h3, td, th { overflow-wrap: break-word; text-wrap: pretty }
x-shape, x-icon, x-embed { display: block }"""


def find_chromium():
    found = os.environ.get("CHROMIUM_PATH")
    if found and Path(found).exists():
        return found
    cache = str(Path.home() / ".cache/ms-playwright")
    for pattern in ("chromium_headless_shell-*/*/chrome-headless-shell", "chromium-*/*/chrome"):
        hits = sorted(glob.glob(f"{cache}/{pattern}"))
        if hits:
            return hits[-1]
    for name in ("chromium", "chromium-browser", "google-chrome"):
        if shutil.which(name):
            return shutil.which(name)
    return None


def text_of(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def density(sid, html):
    """Points and words below the title; a slide over a limit is flagged for a human look."""
    body = re.sub(r"<aside.*?</aside>", "", html, flags=re.S)
    body = re.sub(r"<h[1-3][^>]*>.*?</h[1-3]>", "", body, flags=re.S)
    points = [text_of(m) for m in re.findall(r"<(?:li|p)[^>]*>(.*?)</(?:li|p)>", body, flags=re.S)]
    points = [p for p in points if p and not re.fullmatch(r"\[.*\]", p)]
    words = sum(len(p.split()) for p in points)
    longest = max((len(p.split()) for p in points), default=0)
    figures = len(re.findall(r"<img\b", body))
    over = (len(points) > LIMITS["points"] or longest > LIMITS["words_per_point"]
            or words > LIMITS["words"])
    return (f"  {sid:<18} points {len(points):>2}  longest {longest:>2}w  below-title {words:>3}w  "
            f"pictures {figures:>2}" + ("   OVER" if over else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("deck")
    ap.add_argument("out")
    ap.add_argument("--slides", help="comma-separated slide ids; default every slide in order")
    args = ap.parse_args()
    deck, out = Path(args.deck).resolve(), Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    index = json.loads((deck / "project/deck.json").read_text())
    css = (deck / "project/deck.css").read_text() if (deck / "project/deck.css").exists() else ""
    blobs = {}
    ids_file = deck / "img/blob-ids.txt"
    if ids_file.exists():
        blobs = dict(line.split()[:2] for line in ids_file.read_text().splitlines() if line.strip())
    order = args.slides.split(",") if args.slides else index["order"]
    wide = 1440 if index.get("size") == "4:3" else 1920

    chromium = find_chromium()
    if chromium is None:
        print("no Chromium found (CHROMIUM_PATH, ~/.cache/ms-playwright, PATH): density only")
    print("density (limits: 3 points, 12 words a point, 40 words below the title):")
    shots = []
    for sid in order:
        path = deck / "project/slides" / f"{sid}.html"
        if not path.exists():
            print(f"  {sid}: no file")
            continue
        html = path.read_text()
        print(density(sid, html))
        if chromium is None:
            continue

        def local(match):
            name = blobs.get(match.group(1))
            if not name:
                return match.group(0)
            if not Path(name).suffix:
                name += ".png"
            return f"file://{deck}/img/{name}"

        page = re.sub(r"/?_blob/([0-9a-f]{32})", local, html)
        page = re.sub(r"(<section\b[^>]*?)\shidden\b", r"\1", page)
        page = re.sub(r"<x-embed\b.*?</x-embed>", "<x-embed></x-embed>", page, flags=re.S)
        page = re.sub(r"<script\b.*?</script>", "", page, flags=re.S | re.I)  # nothing runs
        page = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|\S+)", "", page, flags=re.I)
        src = out / f"{sid}.html"
        src.write_text(f'<!doctype html><meta charset="utf-8"><style>{BASE.replace("1920px", f"{wide}px")}'
                       f"\n{css}</style><body>{page}</body>")
        png = out / f"{sid}.png"
        subprocess.run(
            [chromium, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--host-resolver-rules=MAP * ~NOTFOUND",
             "--allow-file-access-from-files", f"--window-size={wide},1080",
             f"--screenshot={png}", f"file://{src}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, check=False)
        if png.exists():
            shots.append(png)
        else:
            print(f"  {sid}: not rendered")
    w, h = wide // 2, 540
    for n in range(0, len(shots), 4):
        sheet = Image.new("RGB", (w * 2 + 15, h * 2 + 15), "#888888")
        for k, shot in enumerate(shots[n:n + 4]):
            sheet.paste(Image.open(shot).resize((w, h)), (5 + (k % 2) * (w + 5), 5 + (k // 2) * (h + 5)))
        name = out / f"sheet-{n // 4 + 1:02d}.png"
        sheet.save(name)
        print(f"sheet {name}: " + ", ".join(s.stem for s in shots[n:n + 4]))
    if not shots and chromium:
        sys.exit("nothing was rendered")


if __name__ == "__main__":
    main()

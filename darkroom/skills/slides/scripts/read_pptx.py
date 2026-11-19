#!/usr/bin/env python3
"""read_pptx.py: read a .pptx (a template or a deck to adopt) without changing it.

    uv run --no-project --with python-pptx==1.0.2 --with pillow \
        python read_pptx.py <deck.pptx> <out folder> [--slides 1,4,7]

Prints, in pixels on a 1920-wide canvas, what is needed to rebuild the deck as web slides:
the look (slide size, theme fonts and colours, master title and body sizes, layout
placeholders) and, per slide, every shape's box, its text runs with size, weight and colour,
and its speaker notes. Each picture is saved to <out folder>/img/ already cropped as the
slide shows it. The same dump is written to <out folder>/pptx-dump.txt.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import sys
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn

A = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def short(value):
    return str(value).split(" ")[0].split(".")[-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pptx")
    ap.add_argument("out")
    ap.add_argument("--slides", help="comma-separated slide numbers; default all")
    args = ap.parse_args()

    out = Path(args.out)
    (out / "img").mkdir(parents=True, exist_ok=True)
    prs = Presentation(args.pptx)
    width, height = prs.slide_width, prs.slide_height
    canvas_h = round(1920 * height / width)
    lines: list[str] = []

    def say(text=""):
        lines.append(text)

    def px(value):
        return round(value * 1920 / width)

    def box(shape):
        if shape.left is None:
            return "inherits"
        return f"({px(shape.left)},{px(shape.top)} {px(shape.width)}x{px(shape.height)})"

    def runs(shape):
        paras = []
        for para in shape.text_frame.paragraphs:
            parts = []
            for run in para.runs:
                font = run.font
                try:
                    colour = str(font.color.rgb) if font.color.type is not None else None
                except (AttributeError, TypeError):
                    colour = "theme"
                size = f"{font.size.pt * 2:g}px" if font.size else "inherit"
                style = "".join(k for k, on in (("b", font.bold), ("i", font.italic)) if on)
                text = run.text.replace("\x0b", "<br>")
                parts.append(f"[{size}{' ' + style if style else ''}"
                             f"{' #' + colour if colour else ''}] {text!r}")
            align = short(para.alignment) if para.alignment else "LEFT"
            paras.append(f"lvl{para.level} {align}: " + (" ".join(parts) or "(empty)"))
        return paras

    def fill_of(shape):
        sp_pr = shape._element.find(qn("p:spPr"))
        if sp_pr is None:
            return ""
        solid = sp_pr.find("a:solidFill", A)
        ln = sp_pr.find("a:ln", A)
        bits = []
        if solid is not None and len(solid):
            bits.append("fill=" + (solid[0].get("val") or ""))
        if ln is not None and ln.find("a:noFill", A) is None and ln.get("w"):
            dash = ln.find("a:prstDash", A)
            bits.append(f"line={int(ln.get('w')) / 12700 * 2:g}px"
                        + (f" {dash.get('val')}" if dash is not None else ""))
        return " ".join(bits)

    seen: dict[str, str] = {}

    def save_picture(shape, tag):
        crop = (shape.crop_left, shape.crop_top, shape.crop_right, shape.crop_bottom)
        im = Image.open(io.BytesIO(shape.image.blob))
        w, h = im.size
        if any(abs(c) > 1e-4 for c in crop):
            im = im.crop((int(w * max(crop[0], 0)), int(h * max(crop[1], 0)),
                          int(w * (1 - max(crop[2], 0))), int(h * (1 - max(crop[3], 0)))))
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA")
        target = max(px(shape.width) * 2, 1)  # twice the shown width is enough
        if im.size[0] > target * 1.2:
            im = im.resize((target, max(1, round(im.size[1] * target / im.size[0]))),
                           Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        digest = hashlib.sha1(buf.getvalue()).hexdigest()
        name = seen.setdefault(digest, tag + ".png")
        if name == tag + ".png":
            (out / "img" / name).write_bytes(buf.getvalue())
        cropped = " cropped" if any(abs(c) > 1e-4 for c in crop) else ""
        return f"img/{name}{cropped}"

    def dump(shapes, tag, depth=0, pictures=True):
        k = 0
        pad = "  " + "  " * depth
        for sh in shapes:
            kind = short(sh.shape_type) if sh.shape_type else "SHAPE"
            ph = f" placeholder:{short(sh.placeholder_format.type)}" if sh.is_placeholder else ""
            head = f"{pad}{kind}{ph} {box(sh)}"
            if sh.shape_type == T.GROUP:
                say(head + "  (children in the group's own coordinates)")
                dump(sh.shapes, tag + "g", depth + 1, pictures)
            elif sh.shape_type == T.PICTURE:
                k += 1
                say(head + (" " + save_picture(sh, f"{tag}_{k}") if pictures else ""))
            elif sh.has_text_frame:
                anchor = short(sh.text_frame.vertical_anchor or "TOP")
                say(f"{head} anchor={anchor} {fill_of(sh)}".rstrip())
                for para in runs(sh):
                    say(f"{pad}    {para}")
            else:
                say(f"{head} {fill_of(sh)}".rstrip())

    # ---- the look
    say(f"# {Path(args.pptx).name}")
    say(f"slide {width / 914400:.2f} x {height / 914400:.2f} in -> canvas 1920 x {canvas_h} px; "
        f"{len(prs.slides)} slides; 1 pt = 2 px")
    for n, master in enumerate(prs.slide_masters, 1):
        say(f"\n## master {n}")
        try:
            theme = etree.fromstring(master.part.part_related_by(RT.THEME).blob)
            fonts = [theme.find(f".//a:{t}/a:latin", A) for t in ("majorFont", "minorFont")]
            say("fonts: " + ", ".join(f.get("typeface") for f in fonts if f is not None))
            scheme = theme.find(".//a:clrScheme", A)
            say("colours: " + ", ".join(
                f"{etree.QName(c).localname}=#{c[0].get('lastClr') or c[0].get('val')}"
                for c in scheme))
        except (KeyError, AttributeError):
            say("theme not readable")
        bg = master._element.find(".//p:bg//a:solidFill", {**A, "p": qn("p:bg")[1:].split("}")[0]})
        if bg is not None and len(bg):
            say("background: " + (bg[0].get("val") or ""))
        for sh in master.placeholders:
            sizes = [e.get("sz") for e in sh._element.iter(qn("a:defRPr")) if e.get("sz")][:3]
            say(f"  {short(sh.placeholder_format.type)} {box(sh)} sizes(px by level): "
                + ", ".join(f"{int(s) / 50:g}" for s in sizes))
        for lay in master.slide_layouts:
            say(f"  layout '{lay.name}':")
            dump(lay.shapes, "layout", 1, pictures=False)

    # ---- the slides
    wanted = {int(x) for x in args.slides.split(",")} if args.slides else None
    for n, slide in enumerate(prs.slides, 1):
        if wanted and n not in wanted:
            continue
        hidden = " HIDDEN" if slide._element.get("show") == "0" else ""
        say(f"\n## slide {n}{hidden}  layout '{slide.slide_layout.name}'")
        dump(slide.shapes, f"s{n:02d}")
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
            say("  NOTES:")
            for line in slide.notes_slide.notes_text_frame.text.replace("\x0b", "\n").splitlines():
                say("    " + line)

    text = "\n".join(lines) + "\n"
    (out / "pptx-dump.txt").write_text(text)
    sys.stdout.write(text)
    print(f"\n{len(seen)} pictures -> {out / 'img'}; dump -> {out / 'pptx-dump.txt'}")


if __name__ == "__main__":
    main()

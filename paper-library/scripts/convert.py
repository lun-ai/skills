#!/usr/bin/env python3
"""Fetch one paper and write its full text as md/<stem>.md with the standard header.

Usage:  python3 convert.py <library-dir> <stem> [--from PATH_OR_URL]

The note notes/<stem>.md must exist first: its title, authors, date and Source go into the
header. Without --from, the note's Source is fetched; for arXiv the HTML version is tried
before the PDF. Figures are dropped. The note's "Full text" and "Fetched" fields are updated.

Backends, best first:  HTML -> pandoc (maths kept as LaTeX where the page provides it)
                       PDF  -> pymupdf4llm if installed, else pdftotext (plain text, no headings)
"""
import datetime
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paperlib import FIELD, parse_note  # noqa: E402

ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})(v\d+)?")
UA = {"User-Agent": "paper-library/1.0 (local research bibliography tool)"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get("Content-Type", "")


def html_to_md(data):
    if not shutil.which("pandoc"):
        sys.exit("pandoc is needed to convert HTML")
    html = data.decode("utf-8", errors="replace")
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for m in soup.find_all("math"):
            alt = m.get("alttext")
            m.replace_with(f"${alt}$" if alt else m.get_text(" ", strip=True))
        for tag in soup(["script", "style", "nav", "header", "footer", "img", "svg", "button", "form", "noscript", "iframe"]):
            tag.decompose()
        body = soup.find("article") or soup.find("main") or soup.body or soup
        html = str(body)
    except ImportError:
        pass
    out = subprocess.run(["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"], input=html.encode(), capture_output=True)
    if out.returncode != 0:
        sys.exit("pandoc failed: " + out.stderr.decode()[:400])
    text = out.stdout.decode("utf-8", errors="replace")
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)       # leftover images
    return re.sub(r"\n{3,}", "\n\n", text).strip(), "pandoc from HTML"


def pdf_to_md(data):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        try:
            import pymupdf4llm
            return pymupdf4llm.to_markdown(f.name, write_images=False).strip(), "pymupdf4llm from PDF"
        except ImportError:
            pass
        if not shutil.which("pdftotext"):
            sys.exit("install pymupdf4llm or pdftotext to convert PDFs")
        out = subprocess.run(["pdftotext", "-layout", "-nopgbrk", f.name, "-"], capture_output=True)
        if out.returncode != 0:
            sys.exit("pdftotext failed: " + out.stderr.decode()[:400])
        return out.stdout.decode("utf-8", errors="replace").strip(), "pdftotext from PDF (plain text, headings not recovered)"


def to_md(data, ctype, name):
    if data[:5] == b"%PDF-" or "pdf" in ctype or name.lower().endswith(".pdf"):
        return pdf_to_md(data)
    return html_to_md(data)


def set_field(path, key, value):
    lines = path.read_text(encoding="utf-8").splitlines()
    last_field = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            break
        m = FIELD.match(line)
        if m:
            last_field = i
            if m.group(1).strip() == key:
                lines[i] = f"- **{key}:** {value}"
                break
    else:
        last_field = len(lines) - 1 if last_field is None else last_field
    if not any(FIELD.match(l) and FIELD.match(l).group(1).strip() == key for l in lines):
        lines.insert((last_field if last_field is not None else 0) + 1, f"- **{key}:** {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = sys.argv[1:]
    src = None
    if "--from" in args:
        i = args.index("--from")
        src = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    root, stem = Path(args[0]), args[1]
    note_path = root / "notes" / f"{stem}.md"
    if not note_path.exists():
        sys.exit(f"write {note_path} first (see templates/paper-note.md)")
    note = parse_note(note_path)
    src = src or note.fields.get("Source", "")
    if not src:
        sys.exit("the note has no Source and no --from was given")

    if Path(src).exists():
        candidates, local = [src], True
    else:
        local = False
        m = ARXIV.search(src)
        candidates = [f"https://arxiv.org/html/{m.group(1)}{m.group(2) or ''}", f"https://arxiv.org/pdf/{m.group(1)}{m.group(2) or ''}"] if m else [src]
    body = backend = used = None
    for c in candidates:
        try:
            data, ctype = (Path(c).read_bytes(), "") if local else fetch(c)
            body, backend = to_md(data, ctype, c)
            if len(body.split()) >= 500 or c == candidates[-1]:
                used = c
                break
        except Exception as e:  # try the next candidate
            print(f"  {c}: {e}")
    if not body:
        sys.exit("nothing could be fetched or converted")

    header = [f"# {note.title}", "",
              f"- **Authors:** {note.fields.get('Authors', '')}",
              f"- **Date:** {note.date}",
              f"- **Source:** {note.fields.get('Source', '')}",
              f"- **Note file:** `notes/{stem}.md`",
              "- **Note:** machine-extracted text; figures removed, tables and math may be imperfect.",
              "", "---", ""]
    (root / "md").mkdir(exist_ok=True)
    out = root / "md" / f"{stem}.md"
    out.write_text("\n".join(header) + body + "\n", encoding="utf-8")
    set_field(note_path, "Full text", f"`md/{stem}.md`")
    set_field(note_path, "Fetched", f"{datetime.date.today().isoformat()}, {backend}, from {used}")
    words = len(body.split())
    print(f"wrote {out}: {words} words, {backend}")
    if words < 500:
        print("WARNING: under 500 words. The page may be a paywall, an abstract page or a failed conversion. Read it before trusting it.")


if __name__ == "__main__":
    main()

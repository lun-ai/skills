"""darkroom: develop markdown posts into a styled, linked blog series.

    uv run --no-project --with markdown==3.7 python build.py init <dir> --series "Name" --parts 3
    uv run --no-project --with markdown==3.7 python build.py <dir>/blog.toml

`init` scaffolds blog.toml, one markdown file per post, fig/ and AUTHOR_GUIDE.md.
Building writes <dir>/site/<out>/index.html for every post and prints checks.
The author-facing rules (what is published, chart blocks, figures) are in AUTHOR_GUIDE.md.
"""
import argparse
import html
import importlib.util
import math
import re
import shutil
import sys
import tomllib
from datetime import date
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SKIP_SECTIONS = ("important notes", "open points", "notes for the build")
SERIES_CLS = ["s1", "s2", "s3", "s4", "s0"]


# ------------------------------------------------------------------ chart primitives
# Minimal text by design: no chart titles, no axis titles unless asked, tick labels only,
# a legend only when there is more than one series. The caption carries the message.

def _t(x, y, s, cls="tick", anchor="start"):
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{html.escape(str(s))}</text>'


def _fmt(v, step=None):
    if step is not None:
        frac = f"{step:.10f}".rstrip("0").split(".")[1]
        return f"{v:.{len(frac)}f}"
    return f"{v:.2f}" if abs(v) < 10 else f"{v:.0f}"


def _ticks(lo, hi, target=5):
    """Round tick values inside [lo, hi], about `target` of them."""
    mag = 10 ** math.floor(math.log10((hi - lo) / target))
    best = None
    for step in (m * mag for m in (1, 2, 2.5, 5, 10, 20)):
        first = math.ceil(lo / step - 1e-9) * step
        vals = [round(first + k * step, 10) for k in range(int((hi - first) / step + 1e-9) + 1)]
        score = (abs(len(vals) - target), -step)
        if best is None or score < best[0]:
            best = (score, vals, step)
    return best[1], best[2]


def _legend(series):
    if len(series) < 2:
        return ""
    return '<div class="legend">' + "".join(
        f'<span><i class="k {c}"></i>{html.escape(n)}</span>' for n, c, *_ in series) + "</div>"


def _figure(svg, caption, legend="", wide=False):
    cap = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
    return f'<figure class="chartbox{" wide" if wide else ""}">{svg}{legend}{cap}</figure>'


def _nums(s):
    return [float(x) for x in re.split(r"[,\s]+", s.strip()) if x]


def chart_bars(spec):
    groups = [g.strip() for g in spec["groups"].split(",")]
    series = [(n, SERIES_CLS[i % len(SERIES_CLS)], _nums(v)) for i, (n, v) in enumerate(spec["series"])]
    lo, hi = _nums(spec.get("y", "")) or [0, max(max(v) for _, _, v in series) * 1.15]
    w, h = 720, int(spec.get("height", 260))
    left, right, top, bot = 48, w - 12, 18, h - 34
    Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    gw = (right - left) / len(groups)
    bw = min(46, gw * 0.72 / len(series))
    p = []
    ticks, step = _ticks(lo, hi)
    for v in ticks:
        p.append(f'<line class="grid" x1="{left}" x2="{right}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>')
        p.append(_t(left - 8, Y(v) + 4, _fmt(v, step), "tick", "end"))
    for val, label in spec.get("ref", []):
        p.append(f'<line class="ref" x1="{left}" x2="{right}" y1="{Y(val):.1f}" y2="{Y(val):.1f}"/>')
        if label:
            p.append(_t(right, Y(val) - 6, label, "tick", "end"))
    show_values = spec.get("values", "on").lower() != "off"
    for gi, g in enumerate(groups):
        cx = left + gw * (gi + .5)
        x = cx - bw * len(series) / 2
        for _, cls, vals in series:
            v = vals[gi]
            p.append(f'<rect class="bar {cls}" x="{x:.1f}" y="{Y(v):.1f}" width="{bw - 3:.1f}" height="{bot - Y(v):.1f}" rx="2"/>')
            if show_values:
                p.append(_t(x + (bw - 3) / 2, Y(v) - 5, _fmt(v), "val", "middle"))
            x += bw
        p.append(_t(cx, bot + 20, g, "tick", "middle"))
    svg = f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(spec.get("caption", "bar chart"))}">{"".join(p)}</svg>'
    return _figure(svg, spec.get("caption", ""), _legend(series))


def chart_lines(spec):
    xs = [x.strip() for x in spec["x"].split(",")]
    panels = spec["panels"] or [("", spec["series"])]
    names = []
    for _, ser in panels:
        for n, _ in ser:
            if n not in names:
                names.append(n)
    cls_of = {n: SERIES_CLS[i % len(SERIES_CLS)] for i, n in enumerate(names)}
    allv = [v for _, ser in panels for _, vals in ser for v in _nums(vals)]
    lo, hi = _nums(spec.get("y", "")) or [min(allv) * 0.95, max(allv) * 1.05]
    n = len(panels)
    w, h = 720, int(spec.get("height", 280))
    gap, left0 = 40, 50
    pw = (w - left0 - 12 - gap * (n - 1)) / n
    top, bot = 26 if any(t for t, _ in panels) else 12, h - 34
    Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    p = []
    for i, (title, ser) in enumerate(panels):
        x0 = left0 + i * (pw + gap)
        X = lambda j, x0=x0: x0 + 16 + j * (pw - 32) / max(1, len(xs) - 1)
        if title:
            p.append(_t(x0, 14, title, "label"))
        ticks, step = _ticks(lo, hi)
        for v in ticks:
            p.append(f'<line class="grid" x1="{x0}" x2="{x0 + pw:.1f}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>')
            if i == 0:
                p.append(_t(x0 - 8, Y(v) + 4, _fmt(v, step), "tick", "end"))
        for val, label in spec.get("ref", []):
            p.append(f'<line class="ref" x1="{x0}" x2="{x0 + pw:.1f}" y1="{Y(val):.1f}" y2="{Y(val):.1f}"/>')
            if label and i == n - 1:
                p.append(_t(x0 + pw, Y(val) - 6, label, "tick", "end"))
        for j, lab in enumerate(xs):
            p.append(_t(X(j), bot + 20, lab, "tick", "middle"))
        for name, vals in ser:
            pts = _nums(vals)
            c = cls_of[name]
            p.append(f'<polyline class="line {c}" points="{" ".join(f"{X(j):.1f},{Y(v):.1f}" for j, v in enumerate(pts))}"/>')
            p += [f'<circle class="dot {c}" cx="{X(j):.1f}" cy="{Y(v):.1f}" r="3.6"/>' for j, v in enumerate(pts)]
    if spec.get("xlabel"):
        p.append(_t(w / 2, h - 2, spec["xlabel"], "tick", "middle"))
    svg = f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(spec.get("caption", "line chart"))}">{"".join(p)}</svg>'
    return _figure(svg, spec.get("caption", ""), _legend([(nm, cls_of[nm]) for nm in names]))


RENDERERS = {"bars": chart_bars, "lines": chart_lines}


def parse_chart_block(body):
    """key: value lines. Repeatable keys: series (`name = values`), ref (`value label`),
    panel (starts a new small multiple)."""
    spec = {"series": [], "ref": [], "panels": []}
    current = None
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "panel":
            current = (val, [])
            spec["panels"].append(current)
        elif key == "series":
            name, _, vals = val.partition("=")
            (current[1] if current else spec["series"]).append((name.strip(), vals.strip()))
        elif key == "ref":
            num, _, label = val.partition(" ")
            spec["ref"].append((float(num), label.strip()))
        else:
            spec[key] = val
    kind = spec.get("type", "bars")
    if kind not in RENDERERS:
        raise SystemExit(f"chart block: unknown type '{kind}' (known: {', '.join(RENDERERS)})")
    return RENDERERS[kind](spec)


# ------------------------------------------------------------------ markdown → html

def front_matter(text):
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            k, sep, v = line.partition(":")
            if sep:
                meta[k.strip()] = v.split("#")[0].strip()
        text = text[m.end():]
    return meta, text


def split_sections(text):
    lines = text.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "Untitled")
    body, keep, started = [], True, False
    for line in lines:
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            started = True
            keep = not line[3:].strip().lower().startswith(SKIP_SECTIONS)
        if started and keep:
            body.append(line)
    return title, "\n".join(body)


def preprocess(md_text, src_dir, custom):
    ph = {}

    def put(snippet):
        key = f"DARKROOMPH{len(ph)}X"
        ph[key] = snippet
        return f"\n\n{key}\n\n"

    md_text = re.sub(r"^```chart[ \t]*\n(.*?)^```[ \t]*$", lambda m: put(parse_chart_block(m.group(1))),
                     md_text, flags=re.S | re.M)

    def named(m):
        name = m.group(1)
        if name not in custom:
            raise SystemExit(f"<!-- chart: {name} --> has no function in charts.py")
        return put(custom[name]())

    md_text = re.sub(r"<!--\s*chart:\s*([\w-]+)\s*-->", named, md_text)

    def svg_include(m):
        path = (src_dir / m.group(1).strip())
        svg = re.sub(r"<\?xml.*?\?>", "", path.read_text(), flags=re.S)
        return put(f'<figure class="chartbox">{svg}<figcaption>{html.escape(m.group(2) or "")}</figcaption></figure>')

    md_text = re.sub(r"<!--\s*svg:\s*([^|>]+?)\s*(?:\|\s*(.*?))?\s*-->", svg_include, md_text)
    md_text = re.sub(r"<!--.*?-->", "", md_text, flags=re.S)
    md_text = re.sub(r"``(.+?)''", r"“\1”", md_text)

    return md_text, ph


def render(md_text, src_dir, custom):
    import markdown
    md_text, ph = preprocess(md_text, src_dir, custom)
    out = markdown.markdown(md_text, extensions=["tables", "md_in_html", "sane_lists", "toc", "fenced_code"])
    for k, v in ph.items():
        out = out.replace(f"<p>{k}</p>", v)
    out = re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>',
                 lambda m: f'<figure class="img"><img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy">'
                           f"<figcaption>{m.group(1)}</figcaption></figure>", out)
    return re.sub(r"(<table>.*?</table>)", r'<div class="tbl">\1</div>', out, flags=re.S)


def toc(body):
    h2 = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    lv = r"h[23]" if len(h2) < 3 else r"h2"
    return "".join(f'<li class="toc-{t}"><a href="#{i}">{x}</a></li>'
                   for t, i, x in re.findall(rf'<({lv}) id="([^"]+)">(.*?)</\1>', body))


def series_nav(parts, current):
    if len(parts) < 2:
        return ""
    lis = []
    for k, (title, url, status) in enumerate(parts, 1):
        badge = ' <span class="tag preliminary">unfinished</span>' if status == "unfinished" else ""
        label = f'<span class="n">Part {k}</span>'
        if k == current:
            lis.append(f'<li aria-current="page">{label}{html.escape(title)}{badge}</li>')
        elif url:
            lis.append(f'<li>{label}<a href="{url}">{html.escape(title)}</a>{badge}</li>')
        else:
            lis.append(f"<li>{label}{html.escape(title)}{badge} <em>(link after first publish)</em></li>")
    return ('<nav class="series col" aria-label="Series"><h2>The series</h2><ol>'
            + "".join(lis) + "</ol></nav>")


def check(page, src, root):
    problems = []
    for pat, what in [(r"\{\{", "template placeholder"), (r"<!--", "HTML comment"),
                      (r"DARKROOMPH", "chart placeholder"), (r"YOUR THINKING|TODO", "author note")]:
        if re.search(pat, page):
            problems.append(what)
    for img in re.findall(r'<img src="([^"]+)"', page):
        if not img.startswith(("http", "data:")) and not (root / img).exists():
            problems.append(f"missing figure {img}")
    print(f"  {src}: " + ("ok" if not problems else "CHECK " + "; ".join(problems)))
    return not problems


def build(toml_path):
    toml_path = Path(toml_path).resolve()
    root = toml_path.parent
    cfg = tomllib.loads(toml_path.read_text())
    s = cfg["series"]
    template = (root / s["template"]).read_text() if s.get("template") else (SKILL / "assets" / "template.html").read_text()
    custom = {}
    if (root / "charts.py").exists():
        spec = importlib.util.spec_from_file_location("charts", root / "charts.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        custom = getattr(mod, "CHARTS", {})
    loaded = []
    for post in cfg["posts"]:
        meta, text = front_matter((root / post["source"]).read_text())
        title, md_text = split_sections(text)
        loaded.append((post, meta, title, md_text))
    parts = [(t, p.get("url", ""), m.get("status", "")) for p, m, t, _ in loaded]
    ok = True
    for k, (post, meta, title, md_text) in enumerate(loaded, 1):
        body = render(md_text, root, custom)
        name = s.get("name", "")
        series_line = "" if not name or name.strip() == title.strip() else \
            f'<p class="series-line">Part of the series: {html.escape(name)}</p>'
        banner = ""
        if meta.get("status") == "unfinished":
            banner = ('<div class="banner"><span class="tag preliminary">unfinished</span> '
                      "This part describes work in progress; the results below are preliminary.</div>")
        built = meta.get("date") or date.today().isoformat()
        try:
            built = date.fromisoformat(built).strftime("%-d %b %Y")
        except ValueError:
            pass
        meta_bits = [f'<span class="kind">{html.escape(s.get("kind", "Research diary"))}</span>']
        if len(loaded) > 1:
            meta_bits.append(f"<span>Part {k} of {len(loaded)}</span>")
        meta_bits.append(f"<span>{built}</span>")
        page = (template.replace("{{TITLE}}", html.escape(title))
                .replace("{{META}}", "".join(meta_bits))
                .replace("{{SERIESLINE}}", series_line if len(loaded) > 1 else "")
                .replace("{{BANNER}}", banner)
                .replace("{{TOC}}", toc(body))
                .replace("{{BODY}}", body)
                .replace("{{SERIESNAV}}", series_nav(parts, k))
                .replace("{{FOOTER}}", s.get("footer", "")))
        out = root / "site" / post["out"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page)
        print(f"wrote {out.relative_to(root)} ({len(page) // 1024} KB)")
        ok &= check(page, post["source"], root)
    return ok


POST_SKELETON = """---
part: {n}
status: draft          # "unfinished" adds a work-in-progress banner
date: {today}          # shown in the meta line above the title
---

# Part {n}: the question this post answers

Working notes (not published): everything between the title and the first `##` heading.

## Important notes for generating the blog HTML

<!-- Requests for the next build go here. This section is never published. -->

## 0. Motivation

Why this question, in a few paragraphs. No date in this heading.

## 1. First thing tried (6–7 Sep 2026)

What was set out to test, how it was set up, what came out, what led to the next step.
At most one table or chart for the key result. See AUTHOR_GUIDE.md.

## References
"""


def init(target, series, parts):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    (target / "fig").mkdir(exist_ok=True)
    today = date.today().isoformat()
    posts = []
    for n in range(1, parts + 1):
        src = target / f"part{n}.md"
        if not src.exists():
            src.write_text(POST_SKELETON.format(n=n, today=today))
        posts.append(f'[[posts]]\nsource = "part{n}.md"\nout = "part{n}"\nurl = ""\n')
    cfg = target / "blog.toml"
    if not cfg.exists():
        cfg.write_text(
            f'[series]\nname = "{series}"\nkind = "Research diary"\nfigures = "fig"\n'
            'footer = ""   # e.g. \'Code: <a href="https://github.com/org/repo">github.com/org/repo</a>\'\n\n'
            + "\n".join(posts))
    shutil.copy(SKILL / "assets" / "AUTHOR_GUIDE.md", target / "AUTHOR_GUIDE.md")
    print(f"scaffolded {target}: blog.toml, {parts} post files, fig/, AUTHOR_GUIDE.md")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("dir")
        ap.add_argument("--series", required=True)
        ap.add_argument("--parts", type=int, default=1)
        a = ap.parse_args()
        init(a.dir, a.series, a.parts)
    elif len(sys.argv) == 2:
        sys.exit(0 if build(sys.argv[1]) else 1)
    else:
        print(__doc__)
        sys.exit(2)

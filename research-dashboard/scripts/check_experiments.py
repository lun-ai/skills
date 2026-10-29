#!/usr/bin/env python3
"""Check the per-experiment files (e###/setup.md, results.md, interpretation.md, checks.md).

Usage: python3 check_experiments.py path/to/DASHBOARD.md [E### ...]

Structural layer of the dashboard-checker: required files per status, links from the
registry, required headings, a Source for every value in setup.md tables, repository paths
that resolve, a "Produced by:" line under every results table, review states on run
sections, numbers in the dashboard and interpretation that do not appear in results.md, and
whether a fact check was logged after the last update. It does not judge whether a value is
right; that is the checker's factual layer (skills/dashboard-checker/SKILL.md).
Exits 1 if any error is found; warnings alone exit 0.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_map import parse, section, status_word, table_rows  # noqa: E402

SETUP_HEADINGS = ["Question", "Lineage and provenance", "Data", "System under test", "Arms",
                  "Held fixed across all arms", "Procedure", "Metrics and derived quantities",
                  "Decision rules", "What this cannot show", "Implementation",
                  "Changes during execution"]
RESULTS_HEADINGS = ["Current results", "Execution notes", "Limitations and what was not done"]
REVIEW_STATE = re.compile(r"reviewed by the user|not yet reviewed|superseded by", re.I)
CAUSAL = re.compile(r"\b(because|suggests?|indicates?|likely|probably|driven by|due to|"
                    r"implies|demonstrates|shows that|explains?)\b", re.I)
NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?%?(?![\w])")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# A Source cell that names a repository path: a token with a slash or a file extension.
PATH_TOKEN = re.compile(r"`?([\w./-]+\.[A-Za-z0-9]{1,6}|[\w.-]+/[\w./-]*)"
                        r"(?::(\d+)(?:-\d+)?)?(?:@([0-9a-f]{7,40}))?`?")
NON_PATH_SOURCE = re.compile(r"^(decision:|job\b|jobs\b|paper\b|.*et al\.|https?:)", re.I)
STAGE = {"planned": 0, "designing": 1, "running": 2, "done": 3, "abandoned": -1}


def headings(text, level=2):
    return [h.strip() for h in re.findall(rf"^{'#' * level} (.+)$", text, re.M)]


def has_heading(text, name):
    return any(h == name or h.startswith(name + " ") or h.startswith(name + " (")
               for h in headings(text))


def tables(text):
    """(start line, header cells, rows, end line) for every Markdown table in `text`."""
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            head, rows = table_rows("\n".join(lines[i:j]))
            out.append((i + 1, head, rows, j))
            i = j
        else:
            i += 1
    return out


def git(root, *args):
    try:
        r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                           timeout=20)
        return r.returncode, r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def repo_root(start):
    code, out = git(start, "rev-parse", "--show-toplevel")
    return Path(out) if code == 0 and out else start


def check_source(cell, root, where, errors, warnings):
    """A Source cell: present, and any repository path in it exists (at the commit, if given)."""
    cell = cell.strip()
    if not cell or cell in ("—", "-", "?"):
        warnings.append(f"{where}: no source ('{cell or 'empty'}'); unverifiable")
        return
    if NON_PATH_SOURCE.match(cell.strip("`")):
        return
    for m in PATH_TOKEN.finditer(cell):
        path, line, commit = m.group(1), m.group(2), m.group(3)
        if re.fullmatch(r"\d+(\.\d+)*", path) or path.startswith("http"):
            continue
        f = root / path
        if commit:
            code, _ = git(root, "cat-file", "-e", f"{commit}:{path}")
            if code != 0:
                errors.append(f"{where}: source {path}@{commit} does not exist at that commit")
            continue
        if not f.exists():
            errors.append(f"{where}: source {path} does not exist")
        elif line and f.is_file():
            n = sum(1 for _ in f.open(errors="replace"))
            if int(line) > n:
                errors.append(f"{where}: source {path}:{line} is past the end ({n} lines)")


def placeholders(path, eid, warnings):
    """Template placeholders (<...>) left outside HTML comments and code."""
    text = re.sub(r"<!--.*?-->|```.*?```|`[^`]*`", "", path.read_text(), flags=re.S)
    text = re.sub(r"<a id=[^>]*></a>", "", text)
    left = re.findall(r"<[^<>\n]{2,80}>", text)
    if left:
        warnings.append(f"{eid}: {path.name} has {len(left)} unfilled template placeholder(s), "
                        f"e.g. {left[0]}")


def numbers(text):
    return {n.rstrip("%").lstrip("-") for n in NUMBER.findall(text)}


def check_experiment(eid, reg_row, status, d, dash, root, errors, warnings):
    num = eid[1:]
    folder = dash.parent / f"e{num}"
    stage = STAGE.get(status_word(status), 0)
    links = reg_row[7] if len(reg_row) > 7 else ""
    files = {k: folder / f"{k}.md" for k in ("setup", "results", "interpretation", "checks")}

    need = {"setup": stage >= 1, "results": stage >= 2}
    for k, required in need.items():
        if required and not files[k].exists():
            errors.append(f"{eid} ({status_word(status)}): e{num}/{k}.md is missing")
    for k, f in files.items():
        rel = f"e{num}/{k}.md"
        if f.exists() and k != "checks" and rel not in links:
            errors.append(f"{eid}: {rel} exists but the registry Links cell does not link it")
        if rel in links and not f.exists():
            errors.append(f"{eid}: registry links {rel}, which does not exist")

    for k in ("setup", "results", "interpretation"):
        if files[k].exists():
            placeholders(files[k], eid, warnings)

    if files["setup"].exists():
        text = files["setup"].read_text()
        if not re.search(rf"^# E{num}\b", text, re.M):
            errors.append(f"{eid}: setup.md title does not start with '# E{num}'")
        for h in SETUP_HEADINGS:
            if not has_heading(text, h):
                errors.append(f"{eid}: setup.md has no '## {h}' section")
        for start, head, rows, _ in tables(text):
            if "source" not in head:
                continue
            col = head.index("source")
            for r in rows:
                if not any(c.strip() for c in r):
                    continue
                key = r[0] if r else "?"
                cell = r[col] if col < len(r) else ""
                if key in ("—", "-") and not cell.strip():
                    continue
                check_source(cell, root, f"{eid} setup.md:{start} '{key}'", errors, warnings)
        commit = re.search(r"Code at `([0-9a-f]{7,40})`", text)
        if commit:
            code, changed = git(root, "diff", "--name-only", commit.group(1), "HEAD", "--")
            cited = {m.group(1) for m in PATH_TOKEN.finditer(text)}
            moved = sorted(set(changed.splitlines()) & cited) if code == 0 else []
            if moved:
                warnings.append(f"{eid}: sources changed since the setup's commit "
                                f"{commit.group(1)}: {', '.join(moved)}")
        elif stage >= 2:
            warnings.append(f"{eid}: setup.md has no 'Code at `<commit>`' line")

    results_text = ""
    if files["results"].exists():
        results_text = text = files["results"].read_text()
        lines = text.splitlines()
        if not re.search(rf"^# E{num}\b", text, re.M):
            errors.append(f"{eid}: results.md title does not start with '# E{num}'")
        for h in RESULTS_HEADINGS:
            if not has_heading(text, h) and not (h == "Current results" and stage < 3):
                errors.append(f"{eid}: results.md has no '## {h}' section")
        for h in headings(text):
            if any(h.startswith(x) for x in RESULTS_HEADINGS):
                continue
            if not REVIEW_STATE.search(h):
                warnings.append(f"{eid}: results.md run section '{h[:60]}' has no review state "
                                "(reviewed by the user <date> / not yet reviewed / superseded by)")
        for start, _, _, end in tables(text):
            after = [l for l in lines[end:end + 6] if l.strip()]
            if not any(l.lstrip().startswith("Produced by:") for l in after[:2]):
                errors.append(f"{eid}: results.md table at line {start} has no 'Produced by:' "
                              "line after it")
        for m in re.finditer(r"^Produced by:(.*)$", text, re.M):
            for p in re.findall(r"`([^`@]+?)`", m.group(1)):
                p = p.strip()
                if "/" in p or "." in p:
                    if not (root / p).exists() and not (folder / p).exists():
                        warnings.append(f"{eid}: results.md produced-by path {p} not found "
                                        "(fine if outputs are git-ignored on another machine)")
        limits = section(text, "## Limitations and what was not done") or ""
        for i, l in enumerate(lines, 1):
            if l in limits or l.startswith("#") or l.startswith("Produced by:"):
                continue
            m = CAUSAL.search(l)
            if m:
                warnings.append(f"{eid}: results.md:{i} causal wording '{m.group(0)}'; "
                                "facts only (move to interpretation.md if it is a claim)")

    if files["interpretation"].exists():
        text = files["interpretation"].read_text()
        claims = section(text, "## Claims") or ""
        for item in re.findall(r"^\d+\.\s+(.+(?:\n(?!\d+\.)\s+.+)*)", claims, re.M):
            if "results.md" not in item:
                warnings.append(f"{eid}: interpretation claim '{item[:50]}...' links no result")
        if results_text:
            stray = numbers(claims) - numbers(results_text)
            if stray:
                warnings.append(f"{eid}: interpretation.md quotes numbers not in results.md: "
                                + ", ".join(sorted(stray)[:8]))

    head, rows = table_rows(section(d["text"], "## Experiments"))
    col = head.index("one-line result") if "one-line result" in head else None
    for r in rows:
        if col is not None and eid in r[0] and results_text and col < len(r):
            stray = numbers(r[col]) - numbers(results_text)
            if stray:
                warnings.append(f"{eid}: dashboard one-line result quotes numbers not in "
                                "results.md: " + ", ".join(sorted(stray)[:8]))

    updated = reg_row[5] if len(reg_row) > 5 else ""
    if stage == 3:
        checked = []
        if files["checks"].exists():
            for _, head, rows, _ in tables(files["checks"].read_text()):
                if head and head[0] == "date":
                    checked += [r[0] for r in rows if DATE.fullmatch(r[0])]
        last = max(checked) if checked else None
        if not last:
            warnings.append(f"{eid}: done but never fact-checked (no e{num}/checks.md entry); "
                            "run the dashboard-checker")
        elif DATE.fullmatch(updated) and last < updated:
            warnings.append(f"{eid}: last fact check {last} is before the last update "
                            f"{updated}; run the dashboard-checker")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    dash = Path(argv[0])
    text = dash.read_text()
    if section(text, "## Research map") is None:
        print(f"ERROR: no '## Research map' section in {dash}")
        return 1
    d = parse(text)
    d["text"] = text
    root = repo_root(dash.parent.resolve())
    wanted = {a.upper() for a in argv[1:]}
    errors, warnings = [], []
    reg_ids = sorted(r for r in d["registry"] if re.fullmatch(r"E\d{3,}", r))
    if reg_ids and not any((dash.parent / f"e{e[1:]}").is_dir() for e in reg_ids):
        print("note: no e###/ folders beside the dashboard, so this dashboard keeps setup and "
              "results in its topic files. Nothing checked. To move it to e###/ files, propose "
              "the migration in references/experiment-files.md to the user.")
        return 0
    for eid in reg_ids:
        if wanted and eid not in wanted:
            continue
        check_experiment(eid, d["registry"][eid], d["listed"].get(eid, ""), d, dash, root,
                         errors, warnings)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    n = len(wanted & set(reg_ids)) if wanted else len(reg_ids)
    print(f"{n} experiment(s) checked on {date.today()}; "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

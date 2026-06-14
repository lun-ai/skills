#!/usr/bin/env python3
"""Discover skill packages under the repo root and emit name/description as JSON.

Usage: python3 list_skills.py [root_dir]
"""
import json
import sys
from pathlib import Path

import yaml


def _first_paragraph(body: str) -> str:
    """Return the first non-heading, non-empty paragraph of markdown body text."""
    for block in body.split("\n\n"):
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        return " ".join(block.split())
    return ""


def parse_skill_md(path: Path) -> dict:
    """Parse a SKILL.md file, falling back gracefully when frontmatter is
    missing, incomplete, or malformed."""
    text = path.read_text(encoding="utf-8")
    has_frontmatter = False
    name = None
    description = None
    body = text

    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            frontmatter_text = text[4:end]
            body = text[end + 4:].lstrip("\n")
            try:
                data = yaml.safe_load(frontmatter_text)
            except yaml.YAMLError:
                data = None
            if isinstance(data, dict):
                fm_name = data.get("name")
                fm_description = data.get("description")
                if fm_name and fm_description:
                    has_frontmatter = True
                    name = fm_name
                    description = fm_description

    if not name:
        name = path.parent.name
    if not description:
        description = _first_paragraph(body)
    if isinstance(description, str):
        description = " ".join(description.split())

    return {
        "name": name,
        "dir": path.parent.name,
        "description": description,
        "has_frontmatter": has_frontmatter,
    }


def discover(root: Path) -> list:
    results = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if skill_md.exists():
            results.append(parse_skill_md(skill_md))
    return results


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    print(json.dumps(discover(root), indent=2, ensure_ascii=False))

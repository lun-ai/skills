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
    """Discover top-level skills and plugin-grouped skill families.

    A top-level directory containing ``.claude-plugin/plugin.json`` plus a
    ``skills/`` folder is a plugin group (e.g. ``nature/``). Each
    ``skills/<name>/SKILL.md`` inside it is emitted with ``name`` prefixed by
    the group (``nature:writing``), ``dir`` set to the repo-relative path
    (``nature/skills/writing``), and ``group`` naming the plugin.
    """
    results = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        skill_md = entry / "SKILL.md"
        if skill_md.exists():
            item = parse_skill_md(skill_md)
            item["group"] = None
            results.append(item)
            continue
        manifest = entry / ".claude-plugin" / "plugin.json"
        skills_dir = entry / "skills"
        if manifest.exists() and skills_dir.is_dir():
            group = json.loads(manifest.read_text(encoding="utf-8")).get("name", entry.name)
            for sub in sorted(skills_dir.iterdir()):
                sub_md = sub / "SKILL.md"
                if sub.is_dir() and sub_md.exists():
                    item = parse_skill_md(sub_md)
                    item["name"] = f"{group}:{item['name']}"
                    item["dir"] = f"{entry.name}/skills/{sub.name}"
                    item["group"] = group
                    results.append(item)
    return results


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    print(json.dumps(discover(root), indent=2, ensure_ascii=False))

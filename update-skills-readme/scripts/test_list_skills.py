import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from list_skills import discover, parse_skill_md


def _write_skill(tmp_path, dirname, content):
    skill_dir = tmp_path / dirname
    skill_dir.mkdir()
    path = skill_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


def test_parses_valid_frontmatter(tmp_path):
    path = _write_skill(tmp_path, "my-skill", (
        "---\n"
        "name: my-skill\n"
        "description: Does a thing.\n"
        "---\n"
        "\n"
        "# My Skill\n"
    ))
    assert parse_skill_md(path) == {
        "name": "my-skill",
        "dir": "my-skill",
        "description": "Does a thing.",
        "has_frontmatter": True,
    }


def test_falls_back_when_no_frontmatter(tmp_path):
    path = _write_skill(tmp_path, "plain-skill", (
        "# Plain Skill\n"
        "\n"
        "This skill explains a concept using a fable.\n"
        "\n"
        "More details follow.\n"
    ))
    result = parse_skill_md(path)
    assert result["name"] == "plain-skill"
    assert result["dir"] == "plain-skill"
    assert result["description"] == "This skill explains a concept using a fable."
    assert result["has_frontmatter"] is False


def test_falls_back_when_frontmatter_missing_description(tmp_path):
    path = _write_skill(tmp_path, "incomplete-skill", (
        "---\n"
        "name: incomplete-skill\n"
        "---\n"
        "\n"
        "Some body text here.\n"
    ))
    result = parse_skill_md(path)
    assert result["name"] == "incomplete-skill"
    assert result["description"] == "Some body text here."
    assert result["has_frontmatter"] is False


def test_falls_back_on_malformed_yaml(tmp_path):
    path = _write_skill(tmp_path, "broken-skill", (
        "---\n"
        "name: broken-skill\n"
        "description: [unclosed\n"
        "---\n"
        "\n"
        "Body paragraph for broken skill.\n"
    ))
    result = parse_skill_md(path)
    assert result["name"] == "broken-skill"
    assert result["description"] == "Body paragraph for broken skill."
    assert result["has_frontmatter"] is False


def test_discover_finds_skill_directories(tmp_path):
    _write_skill(tmp_path, "skill-a", "---\nname: skill-a\ndescription: A skill.\n---\n")
    _write_skill(tmp_path, "skill-b", "---\nname: skill-b\ndescription: B skill.\n---\n")
    not_a_skill = tmp_path / "not-a-skill"
    not_a_skill.mkdir()
    (not_a_skill / "README.md").write_text("nope", encoding="utf-8")

    results = discover(tmp_path)
    assert [r["name"] for r in results] == ["skill-a", "skill-b"]


def test_cli_outputs_json(tmp_path):
    _write_skill(tmp_path, "skill-a", "---\nname: skill-a\ndescription: A skill.\n---\n")
    script = Path(__file__).resolve().parent / "list_skills.py"
    output = subprocess.run(
        [sys.executable, str(script), str(tmp_path)],
        capture_output=True, text=True, check=True,
    ).stdout
    data = json.loads(output)
    assert data[0]["name"] == "skill-a"

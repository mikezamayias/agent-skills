#!/usr/bin/env python3
"""Validate the skill packages under skills/."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# Agent Skills specification keys (https://agentskills.io/specification).
ALLOWED_KEYS = {
    "allowed-tools",
    "compatibility",
    "description",
    "license",
    "metadata",
    "name",
}


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


SENTENCE_LIMIT = 3
ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "vs.", "approx.", "Inc.", "Ltd.")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


def count_sentences(text: str) -> int:
    """Approximate sentence count for a description.

    Parenthetical asides and common abbreviations would otherwise split a single
    sentence into several, so both are neutralised before splitting.
    """
    flattened = re.sub(r"\([^()]*\)", "", " ".join(text.split()))
    for abbreviation in ABBREVIATIONS:
        flattened = flattened.replace(abbreviation, abbreviation.replace(".", "․"))
    return len([part for part in SENTENCE_SPLIT.split(flattened) if part.strip()])


def local_link_errors(skill_file: Path) -> list[str]:
    errors: list[str] = []
    text = skill_file.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for raw_target in MARKDOWN_LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("#", "/", "mailto:", "http://", "https://")):
            continue
        target = unquote(target)
        if not (skill_file.parent / target).exists():
            errors.append(f"missing local link: {raw_target}")
    return errors


def docs_verified_errors(data: dict) -> list[str]:
    """Check metadata.docs-verified, the date the skill was last checked against official docs."""
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or "docs-verified" not in metadata:
        return []
    value = metadata["docs-verified"]
    # Spec metadata values are strings, so the date must be quoted in YAML.
    if not isinstance(value, str):
        return [f"docs-verified must be a quoted YYYY-MM-DD string, got {value!r}"]
    try:
        verified = date.fromisoformat(value)
    except ValueError:
        return [f"docs-verified is not a YYYY-MM-DD date: {value}"]
    if verified > date.today():
        return [f"docs-verified is in the future: {value}"]
    return []


def validate() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    names: defaultdict[str, list[str]] = defaultdict(list)
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())

    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{directory.name}: missing exact-case SKILL.md")
            continue

        try:
            data = parse_frontmatter(skill_file)
        except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
            errors.append(f"{directory.name}: {exc}")
            continue

        unknown = sorted(set(data) - ALLOWED_KEYS)
        if unknown:
            errors.append(f"{directory.name}: unsupported frontmatter keys: {', '.join(unknown)}")

        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name:
            errors.append(f"{directory.name}: missing string name")
        else:
            names[name].append(directory.name)
            if not NAME_PATTERN.fullmatch(name):
                errors.append(f"{directory.name}: invalid canonical name: {name}")
            if name != directory.name:
                errors.append(f"{directory.name}: frontmatter name differs: {name}")

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{directory.name}: missing string description")
        elif len(description) > 1024:
            errors.append(f"{directory.name}: description exceeds 1024 characters")
        else:
            # Descriptions are injected into every session on every agent, so
            # they state what the skill does and when to fire it. Implementation
            # detail belongs in the body. Advisory, not a build failure.
            sentences = count_sentences(description)
            if sentences > SENTENCE_LIMIT:
                warnings.append(
                    f"{directory.name}: description is {sentences} sentences "
                    f"(limit {SENTENCE_LIMIT}); move detail into the body"
                )

        errors.extend(f"{directory.name}: {message}" for message in docs_verified_errors(data))
        errors.extend(f"{directory.name}: {message}" for message in local_link_errors(skill_file))

    for name, directories in sorted(names.items()):
        if len(directories) > 1:
            errors.append(f"duplicate canonical name {name}: {', '.join(directories)}")

    return errors, warnings


def main() -> int:
    errors, warnings = validate()
    skill_count = sum(1 for path in SKILLS.iterdir() if path.is_dir())
    print(f"skills={skill_count} errors={len(errors)} warnings={len(warnings)}")
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

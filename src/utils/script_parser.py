from typing import Dict, List

from src.models.types import Section


def parse_script_plan(content: str) -> List[Section]:
    """Parse the script plan content into structured sections."""
    sections = []
    current_section = None
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    for line in lines:
        if line.startswith("##"):
            if current_section:
                sections.append(current_section)

            current_section = {"title": line.lstrip("#").strip(), "points": []}

        elif line.startswith("-"):
            if current_section:
                current_section["points"].append(line.lstrip("- ").strip())

    if current_section:
        sections.append(current_section)

    return sections

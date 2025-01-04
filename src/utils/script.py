from typing import Dict, List

from src.utils.reddit import format_comments
from src.utils.urls import format_url_content


def format_posts_for_script(posts: List[Dict]) -> str:
    """Format processed posts for script generation."""
    formatted = []
    for i, post in enumerate(posts, 1):
        formatted.append(
            f"""
        Post {i}:
        Title: {post['title']}
        Summary: {post['summary']}

        Key Points from Related Content:
        {format_url_content(post.get('url_content', {}))}

        Notable Discussion:
        {format_comments(post.get('top_comments', []))}

        ---
        """
        )
    return "\n".join(formatted)


def parse_script_plan(content: str) -> list[dict]:
    """
    Parse the script plan content into structured sections.

    Args:
        content: String containing the script plan with headers and bullet points

    Returns:
        List of dictionaries containing parsed sections with title and discussion points
    """
    sections = []
    current_section = None

    # Split into lines and remove any empty lines
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    for line in lines:
        # Check if line is a header (starts with ##)
        if line.startswith("##"):
            # If we have a previous section, add it
            if current_section:
                sections.append(current_section)

            # Start new section
            current_section = {"title": line.lstrip("#").strip(), "points": []}

        # Check if line is a bullet point
        elif line.startswith("-"):
            if current_section:
                current_section["points"].append(line.lstrip("- ").strip())

    # Add the last section
    if current_section:
        sections.append(current_section)

    return sections

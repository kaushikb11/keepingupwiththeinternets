from typing import Dict, List

from src.components.base import BaseComponent
from src.models.types import Section
from src.prompts.dialogue import INTRODUCTION_PROMPT, SECTION_DIALOGUE_PROMPT
from src.utils.formatting import format_comments, format_url_content


class DialogueGenerator(BaseComponent):
    """Component for generating podcast dialogue."""

    def generate_introduction(
        self, sections: List[Section], processed_posts: List[Dict]
    ) -> str:
        """Generate the podcast introduction."""
        context_parts = []
        for section in sections:
            matching_post = next(
                (
                    post
                    for post in processed_posts
                    if section["title"].lower() in post["title"].lower()
                ),
                None,
            )
            if matching_post:
                context_parts.append(
                    f"""
                    Topic: {section['title']}
                    Summary: {matching_post['summary']}"""
                )

        context = "\n\n".join(context_parts)
        return self.openai_service.generate_completion(
            INTRODUCTION_PROMPT.format(context=context)
        )

    def generate_section_dialogue(
        self, section: Section, processed_posts: List[Dict]
    ) -> Dict[str, str]:
        """Generate dialogue for a single section."""
        matching_post = next(
            (
                post
                for post in processed_posts
                if section["title"].lower() in post["title"].lower()
            ),
            None,
        )

        additional_context = ""
        if matching_post:
            additional_context = f"""
            Relevant Context:
            Title: {matching_post['title']}
            Summary: {matching_post['summary']}

            Key URLs and their content:
            {format_url_content(matching_post['url_content'])}

            Top Comments:
            {format_comments(matching_post['comments'])}
            """

        dialogue = self.openai_service.generate_completion(
            SECTION_DIALOGUE_PROMPT.format(
                title=section["title"],
                points="\n".join(f"- {point}" for point in section["points"]),
                context=additional_context,
            )
        )
        return {"dialogue": dialogue}

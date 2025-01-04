from typing import Dict, List, Tuple

from src.components.base import BaseComponent
from src.models.types import Section
from src.prompts.script_planning import SCRIPT_PLAN_PROMPT
from src.utils.formatting import format_posts_for_script
from src.utils.script_parser import parse_script_plan


class ScriptPlanner(BaseComponent):
    """Component for planning podcast scripts from processed posts."""

    def generate_plan(self, processed_posts: List[Dict]) -> Tuple[str, List[Section]]:
        formatted_posts = format_posts_for_script(processed_posts)
        response = self.openai_service.generate_completion(
            SCRIPT_PLAN_PROMPT.format(posts=formatted_posts)
        )
        sections = parse_script_plan(response)
        return response, sections

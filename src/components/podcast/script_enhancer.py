from typing import Dict, List

from src.components.base import BaseComponent
from src.prompts.dialogue import SCRIPT_ENHANCEMENT_PROMPT


class ScriptEnhancer(BaseComponent):
    """Component for enhancing and formatting the final podcast script."""

    def enhance_script(self, introduction: str, dialogues: List[Dict[str, str]]) -> str:
        """Enhance the podcast script by improving transitions and reducing redundancy."""
        full_script = introduction + "\n\n"
        for dialogue in dialogues:
            full_script += f"{dialogue['dialogue']}\n\n"

        prompt = SCRIPT_ENHANCEMENT_PROMPT.format(script=full_script)
        return self.openai_service.generate_completion(prompt)

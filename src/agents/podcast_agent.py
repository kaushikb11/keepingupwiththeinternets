from typing import Dict, List

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from src.components.podcast import (
    DialogueGenerator,
    PodcastGenerator,
    ScriptEnhancer,
    ScriptPlanner,
)
from src.components.reddit import RedditPostFetcher, RedditPostProcessor
from src.models.types import ProcessingState


class PodcastAgent:
    """Agent for orchestrating the podcast generation process"""

    def __init__(self):
        self.post_fetcher = RedditPostFetcher()
        self.post_processor = RedditPostProcessor()
        self.script_planner = ScriptPlanner()
        self.dialogue_generator = DialogueGenerator()
        self.script_enhancer = ScriptEnhancer()
        self.podcast_generator = PodcastGenerator()
        self.workflow = self._create_workflow()

    def fetch_posts(self, state: ProcessingState) -> Dict:
        """Fetch top posts from subreddit."""
        posts = self.post_fetcher.fetch_top_posts(
            subreddit=state["subreddit"],
        )
        return {"posts": posts}

    def process_post(self, state: ProcessingState) -> Dict:
        """Process a single post."""
        return self.post_processor.process_post(state["post"])

    def generate_plan(self, state: ProcessingState) -> Dict:
        """Generate script plan from processed posts."""
        plan, sections = self.script_planner.generate_plan(state["processed_posts"])
        return {"script_plan": plan, "sections": sections}

    def generate_introduction(self, state: ProcessingState) -> Dict:
        """Generate podcast introduction."""
        intro = self.dialogue_generator.generate_introduction(
            state["sections"], state["processed_posts"]
        )
        return {"introduction": intro}

    def generate_dialogue(self, state: ProcessingState) -> Dict:
        """Generate dialogue for a section."""
        dialogue = self.dialogue_generator.generate_section_dialogue(
            state["section"], state["processed_posts"]
        )
        return {"dialogues": [dialogue]}

    def enhance_script(self, state: ProcessingState) -> Dict:
        """Enhance and format the final script."""
        enhanced = self.script_enhancer.enhance_script(
            state["introduction"], state.get("dialogues", [])
        )
        return {"final_script": enhanced}

    def generate_podcast(self, state: ProcessingState) -> Dict:
        """Generate podcast audio."""
        audio_path = self.podcast_generator.generate_podcast(state["final_script"])
        return {"audio_path": audio_path}

    def map_to_post_processing(self, state: ProcessingState) -> List[Send]:
        """Map each post to parallel processing."""
        return [Send("process_post", {"post": post}) for post in state["posts"]]

    def map_to_dialogue_processing(self, state: ProcessingState) -> List[Send]:
        """Map each section to parallel dialogue processing."""
        return [
            Send(
                "generate_dialogue",
                {"section": section, "processed_posts": state["processed_posts"]},
            )
            for section in state["sections"]
        ]

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(ProcessingState)

        workflow.add_node("fetch_posts", self.fetch_posts)
        workflow.add_node("process_post", self.process_post)
        workflow.add_node("generate_plan", self.generate_plan)
        workflow.add_node("generate_introduction", self.generate_introduction)
        workflow.add_node("generate_dialogue", self.generate_dialogue)
        workflow.add_node("enhance_script", self.enhance_script)
        workflow.add_node("generate_podcast", self.generate_podcast)

        workflow.add_edge(START, "fetch_posts")
        workflow.add_conditional_edges(
            "fetch_posts", self.map_to_post_processing, ["process_post"]
        )
        workflow.add_edge("process_post", "generate_plan")
        workflow.add_edge("generate_plan", "generate_introduction")
        workflow.add_conditional_edges(
            "generate_plan", self.map_to_dialogue_processing, ["generate_dialogue"]
        )
        workflow.add_edge("generate_dialogue", "enhance_script")
        workflow.add_edge("enhance_script", "generate_podcast")
        workflow.add_edge("generate_podcast", END)

        return workflow.compile()

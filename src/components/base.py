from src.services.firecrawl import FirecrawlService
from src.services.openai import OpenAIService
from src.services.reddit import RedditService


class BaseComponent:
    """Base component with access to all services."""

    def __init__(self):
        self.openai_service = OpenAIService()
        self.reddit_service = RedditService()
        self.firecrawl_service = FirecrawlService()

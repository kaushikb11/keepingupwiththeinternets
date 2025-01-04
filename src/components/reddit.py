from typing import Dict, List

from src.components.base import BaseComponent
from src.models.types import PostContent
from src.prompts.summary import SUMMARY_PROMPT
from src.utils.formatting import format_comments
from src.utils.urls import extract_urls, format_url_content, is_valid_url


class RedditPostFetcher(BaseComponent):
    def fetch_top_posts(
        self,
        subreddit: str,
        flair_filter: str = "Answered",
        time_filter: str = "week",
        limit: int = 10,
    ) -> List[Dict]:
        return self.reddit_service.get_top_posts(
            subreddit_name=subreddit,
            flair_filter=flair_filter,
            time_filter=time_filter,
            limit=limit,
        )


class RedditPostProcessor(BaseComponent):
    def _generate_summary(self, post: Dict, url_content: Dict[str, str]) -> str:
        prompt = SUMMARY_PROMPT.format(
            title=post["title"],
            content=post["selftext"],
            url_content=format_url_content(url_content),
            comments=format_comments(post["comments"]),
        )
        return self.openai_service.generate_completion(prompt)

    def process_post(self, post: Dict) -> PostContent:
        """Process a single post and its related content."""
        urls = extract_urls(post["selftext"])
        if post["url"] and is_valid_url(post["url"]):
            urls.append(post["url"])

        for comment in post["comments"]:
            urls.extend(extract_urls(comment["body"]))

        urls = list(set(filter(is_valid_url, urls)))
        url_content = self.firecrawl_service.process_urls_batch(urls)

        summary = self._generate_summary(post, url_content)

        return PostContent(
            title=post["title"],
            selftext=post["selftext"],
            url=post["url"],
            comments=post["comments"],
            extracted_urls=urls,
            url_content=url_content,
            summary=summary,
        )

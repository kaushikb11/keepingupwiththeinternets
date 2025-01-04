import logging
import os
from typing import Dict, List

import praw
from dotenv import load_dotenv


class RedditService:
    """Service for interacting with Reddit API."""

    def __init__(self):
        self._client = self._setup_client()

    def _setup_client(self) -> praw.Reddit:
        """Initialize Reddit client with credentials."""
        load_dotenv()

        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")

        if not all([client_id, client_secret, user_agent]):
            raise ValueError(
                "Missing required environment variables. Please ensure REDDIT_CLIENT_ID, "
                "REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are set in your .env file."
            )

        return praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )

    def get_top_posts(
        self,
        subreddit_name: str,
        flair_filter: str = "Answered",
        time_filter: str = "week",
        sort_by: str = "top",
        limit: int = 10,
        max_comments_per_post: int = 3,
    ) -> List[Dict]:
        """Fetch top posts from specified subreddit."""
        subreddit = self._client.subreddit(subreddit_name)

        search_query = f"flair:{flair_filter}" if flair_filter else ""
        posts = []

        try:
            for post in subreddit.search(
                search_query, sort=sort_by, time_filter=time_filter, limit=limit
            ):
                posts.append(self._format_post(post, max_comments_per_post))
            return posts
        except Exception as e:
            logging.error(f"Error fetching posts from r/{subreddit_name}: {str(e)}")
            raise

    def _format_post(self, post: praw.models.Submission, max_comments: int) -> Dict:
        """Format a Reddit post and its comments."""
        top_comments = []
        post.comments.replace_more(limit=0)

        for comment in post.comments:
            if len(top_comments) >= max_comments:
                break
            if not comment.stickied:
                top_comments.append(
                    {
                        "body": comment.body,
                        "score": comment.score,
                        "author": str(comment.author),
                    }
                )

        return {
            "subreddit": str(post.subreddit),
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "author": str(post.author),
            "created_utc": post.created_utc,
            "selftext": post.selftext,
            "comments": top_comments,
        }

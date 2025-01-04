import os
from typing import Dict, List

import praw
from dotenv import load_dotenv


def setup_reddit_client() -> praw.Reddit:
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


def format_comments(comments: List[Dict]) -> str:
    """Format comments for prompts."""
    return "\n".join(
        [
            f"- {comment['author']} (Score: {comment['score']}): {comment['body']}"
            for comment in comments
        ]
    )

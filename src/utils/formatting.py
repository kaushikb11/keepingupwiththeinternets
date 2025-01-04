from typing import Dict, List


def format_comments(comments: List[Dict]) -> str:
    """Format comments for prompts."""
    return "\n".join(
        [
            f"- {comment['author']} (Score: {comment['score']}): {comment['body']}"
            for comment in comments
        ]
    )


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
        {post.get('url_content', 'No additional content available')}

        Notable Discussion:
        {format_comments(post.get('comments', []))}

        ---
        """
        )
    return "\n".join(formatted)


def format_url_content(url_content: Dict[str, str]) -> str:
    """Format URL content for prompts."""
    formatted = []
    for url, content in url_content.items():
        formatted.append(
            f"URL: {url}\nContent: {content[:500]}..."
        )  # Truncate long content
    return "\n\n".join(formatted)

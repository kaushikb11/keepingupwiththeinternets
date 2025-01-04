import logging
import re
from typing import Dict, List
from urllib.parse import urlparse


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text content."""
    url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    urls = re.findall(url_pattern, text)
    return [url for url in urls if is_valid_url(url)]


def is_valid_url(url: str) -> bool:
    """Validate URL and check if it's worth processing."""
    try:
        result = urlparse(url)
        excluded_domains = {
            "imgur.com",
            "i.redd.it",
            "twitter.com",
            "x.com",
            "facebook.com",
            "instagram.com",
            "reddit.com",
            "t.co",
            "youtube.com",
        }
        domain = result.netloc.lower()
        if any(excluded in domain for excluded in excluded_domains):
            logging.info(f"Skipping unsupported/excluded domain: {domain}")
            return False

        return all([result.scheme, result.netloc])
    except Exception as e:
        logging.warning(f"Error validating URL {url}: {str(e)}")
        return False


def format_url_content(url_content: Dict[str, str]) -> str:
    """Format URL content for prompts."""
    formatted = []
    for url, content in url_content.items():
        formatted.append(
            f"URL: {url}\nContent: {content[:500]}..."
        )  # Truncate long content
    return "\n\n".join(formatted)

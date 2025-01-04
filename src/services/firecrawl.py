import logging
import os
import time
from typing import Dict, Optional

from firecrawl import FirecrawlApp
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential


class FirecrawlService:
    """Service for interacting with Firecrawl API."""

    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self._client = FirecrawlApp(api_key=api_key)

    @staticmethod
    def _is_rate_limit_error(exception: Exception) -> bool:
        """Check if the error is due to rate limiting."""
        return "Rate limit exceeded" in str(exception)

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3),
        retry=retry_if_exception(_is_rate_limit_error),
    )
    def fetch_url_content(self, url: str) -> Optional[str]:
        """Fetch content from a URL with retry logic."""
        try:
            response = self._client.scrape_url(url)

            if isinstance(response, dict):
                metadata = response.get("data", {}).get("metadata", {})
                if metadata.get("statusCode") == 404:
                    logging.warning(f"404 Not Found for URL: {url}")
                    return None
                elif metadata.get("pageError"):
                    logging.warning(f"Page error for {url}: {metadata['pageError']}")
                    return None

                return (
                    response.get("markdown")
                    or response.get("data", {}).get("markdown")
                    or response.get("data", {}).get("content")
                )

            elif hasattr(response, "data"):
                return getattr(response.data, "markdown", None) or getattr(
                    response.data, "content", None
                )

            return None

        except Exception as e:
            if self._is_rate_limit_error(e):
                logging.warning(f"Rate limit hit for {url}, retrying...")
                raise
            logging.error(f"Error fetching content for URL {url}: {str(e)}")
            return None

    def process_urls_batch(self, urls: list[str]) -> Dict[str, str]:
        """Process a batch of URLs with rate limiting."""
        url_content = {}

        for url in urls:
            try:
                content = self.fetch_url_content(url)
                if content:
                    url_content[url] = content
                    time.sleep(0.1)
            except Exception as e:
                logging.error(f"Failed to process URL {url} after retries: {str(e)}")
                continue

        return url_content

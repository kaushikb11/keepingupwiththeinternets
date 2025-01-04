import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI


class OpenAIService:
    """Service for interacting with Azure OpenAI API."""

    def __init__(self):
        self._model = self._setup_model()

    def _setup_model(self) -> AzureChatOpenAI:
        """Initialize Azure OpenAI model."""
        load_dotenv()

        deployment = os.getenv("AZURE_DEPLOYMENT")
        api_version = os.getenv("AZURE_API_VERSION")

        if not all([deployment, api_version]):
            raise ValueError(
                "Missing required environment variables. Please ensure AZURE_DEPLOYMENT "
                "and AZURE_API_VERSION are set in your .env file."
            )

        return AzureChatOpenAI(
            azure_deployment=deployment,
            api_version=api_version,
        )

    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Dict[str, Any],
    ) -> str:
        """Generate completion from prompt."""
        try:
            response = self._model.invoke(
                prompt, temperature=temperature, max_tokens=max_tokens, **kwargs
            )
            return response.content
        except Exception as e:
            logging.error(f"Error generating completion: {str(e)}")
            raise

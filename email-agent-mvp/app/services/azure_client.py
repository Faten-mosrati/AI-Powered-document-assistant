from openai import AsyncAzureOpenAI
from app.config import settings


_client: AsyncAzureOpenAI | None = None


def get_client() -> AsyncAzureOpenAI:
    """Singleton Async client.

    Why async: FastAPI handlers are async, and Azure calls are I/O-bound (50ms–5s).
    A sync client would block the event loop and serialize all requests.

    Why singleton: the SDK manages a connection pool internally; creating a new client
    per request defeats that and adds overhead.
    """
    global _client
    if _client is None:
        _client = AsyncAzureOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
        )
    return _client

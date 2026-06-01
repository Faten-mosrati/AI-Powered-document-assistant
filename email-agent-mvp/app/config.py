from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from .env. Pydantic validates that everything required is present
    at startup — if a key is missing, the service won't boot, which is what you want.
    Better to fail at startup than to discover a missing key mid-request."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str = "2024-08-01-preview"
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str = "text-embedding-3-large"


settings = Settings()

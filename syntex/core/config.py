from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # api settings
    app_name: str = "syntex"
    debug_mode: bool = False

    # llm configuration
    openai_api_key: str = ""
    model_name: str = "gpt-4o"

    # vector store settings
    chroma_db_dir: str = "./data/chroma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

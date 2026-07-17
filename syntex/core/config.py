from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # api settings
    app_name: str = "syntex"
    debug_mode: bool = False

    # llm configuration
    openai_api_key: str = ""
    model_name: str = "gpt-4o"

    # vector store settings
    chroma_db_dir: str = "./data/chroma"

    class Config:
        # load variables from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

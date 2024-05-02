from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    chat_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
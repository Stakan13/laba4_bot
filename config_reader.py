from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    indexes_url: SecretStr
    index_id: SecretStr
    user: SecretStr
    port: SecretStr
    password: SecretStr
    host: SecretStr
    database: SecretStr
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")


config = Settings()

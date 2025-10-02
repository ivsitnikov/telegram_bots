from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="settings/.env", env_file_encoding="utf-8", extra="ignore"
    )


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_")
    bot_token: SecretStr
    api_id: SecretStr


class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()

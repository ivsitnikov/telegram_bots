from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", encoding="utf-8", extra="ignore")


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TG_")
    bot_token: SecretStr


class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()

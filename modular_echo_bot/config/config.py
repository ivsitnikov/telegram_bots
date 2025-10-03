from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TG_")
    bot_token: SecretStr


class LoggerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="LOG_")
    level: str
    format: str


class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    log: LoggerConfig = Field(default_factory=LoggerConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


if __name__ == "__main__":
    config = Config.load()
    print(f"{config.telegram}")
    print(f"{config.log.level}")
    print(f"{config.log.format}")

from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class TelegramBotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TG_")
    bot_token: SecretStr


class Config(BaseSettings):
    telegram: TelegramBotConfig = Field(default_factory=TelegramBotConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


if __name__ == "__main__":
    config = Config.load()
    print(f"{config.telegram}")

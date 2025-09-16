from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='tg_')
    bot_token: SecretStr
    api_id: SecretStr
 

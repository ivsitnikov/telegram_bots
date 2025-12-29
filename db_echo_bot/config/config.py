from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings): 
    model_config = SettingsConfigDict(env_file =".env", env_file_encoding="utf-8", extra="ignore")

    
class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TG_") 
    bot_token: SecretStr
    admin_ids: SecretStr


class LoggerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="LOG_")    
    level: str
    format: str


class PostgresConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_") 
    db: str 
    host: str 
    port: str
    user: SecretStr
    password: SecretStr

    
class PgAdminConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="PGADMIN_")
    default_email: SecretStr
    default_password: SecretStr
    

class RedisConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    user_name: SecretStr
    password: SecretStr 
    host: str
    port: str
    database: int


class Config(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    pgadmin: PgAdminConfig = Field(default_factory=PgAdminConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    
    @classmethod
    def load(cls) -> "Config":
        return cls()

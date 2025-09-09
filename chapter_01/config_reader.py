from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretString
    # для конфиденциальных данных типа токена бота
    bot_token: SecretStr

    # Со второй версии Pydantic для настройки класса настроек
    # задаются через model_config
    # в данном случае будет использован файл .env, который прочитан
    # с кодировкой UTF-8
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


# При импорте файла сразу создастся
# и провалидируется объект конфига
# который далее можно импортировать из разных мест
config = Settings()

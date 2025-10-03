import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config
from handlers import user, other


logger = logging.getLogger(__name__)


async def main() -> None:
    # Загружаем конфигурационные данные
    config: Config = Config.load()
    logger.info("Загрузка конфигурационных данных")
    # Конфигурируем логгирование
    logging.basicConfig(
        level=config.log.level,
        format=config.log.format,
        style="{",
    )
    # Инициализация хранилища
    storage = ...

    # Инициализируем диспетчер
    # dp = Dispatcher(storage=storage)

    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(other.router)
    bot = Bot(
        token=config.telegram.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Инициализируем другие объекты (пул соединений с БД, кэш и т.п.)
    # ...
    # Помещаем нужные объекты в workflow_data диспетчера
    # dp.workflow_data.update(...)

    # Настраиваем главное меню бота (сдесь делать это не обязательно)
    # так как главное меню бота может отличаться от роли пользователя
    # и языка ввода
    # await set_main_menu(bot)

    # Регистрируем роутеры
    logger.info("Подключаем роутеры")

    # Подключаем мидлвари

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())

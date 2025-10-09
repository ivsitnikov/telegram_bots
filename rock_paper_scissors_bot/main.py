import logging
import asyncio
from aiogram import Dispatcher, Bot

from config import Config
from handlers import user_router, other_router
from keyboards import set_main_menu


logging.basicConfig(level=logging.INFO, style="{")


async def main():
    logger = logging.getLogger(__name__)
    config = Config.load()
    logger.info(f"Конфигурационные данные для telegram: {config.telegram}")

    bot = Bot(token=config.telegram.bot_token.get_secret_value())

    # Инициализируем объект диспетсера
    dp = Dispatcher()

    # Устанавливаем основное меню
    await set_main_menu(bot)

    # Добавляем роутеры
    dp.include_router(user_router)
    dp.include_router(other_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

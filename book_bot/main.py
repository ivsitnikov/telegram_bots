import logging
import asyncio

from aiogram import Bot, Dispatcher

from config import Config


async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Загружаем конфигурационные данные бота
    config = Config.load()

    bot = Bot(token=config.telegram.bot_token.get_secret_value())
    dispatcher = Dispatcher()

    # Запуск бота
    logger.info(f"Запуск бота")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

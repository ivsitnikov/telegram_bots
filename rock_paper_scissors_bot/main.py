import logging
import asyncio
from aiogram import Dispatcher, Bot

from config import Config


logging.basicConfig(level=logging.INFO, style="{")


async def main():
    logger = logging.getLogger(__name__)
    config = Config.load()
    logger.info(f"Конфигурационные данные для telegram: {config.telegram}")

    dp = Dispatcher()
    bot = Bot(token=config.telegram.bot_token.get_secret_value())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

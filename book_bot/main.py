import logging
import asyncio

from aiogram import Bot, Dispatcher

from config import Config
from keyboards import set_menu
from database import db_init
from handlers import user_router
from services import prepare_book


async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # Загружаем конфигурационные данные бота
    config = Config.load()

    bot = Bot(token=config.telegram.bot_token.get_secret_value())
    dispatcher = Dispatcher()

    # Подготавливаем книгу
    logger.info(f"Prepare book")
    book: str = prepare_book("book/book.txt")

    # Инициализируем "базу данных" проекта
    db = db_init()

    # Добавляем базу данных и книгу в базу данных
    dispatcher.workflow_data.update(book=book, db=db)
    # Установка основного меню бота
    await set_menu(bot=bot)

    # Подключение дополнительных роутеров
    dispatcher.include_router(user_router)
    # Запуск бота
    logger.info(f"Запуск бота")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

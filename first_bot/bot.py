import os
import dotenv
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логгирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Получим переменные окружения

dotenv.load_dotenv()
# Объект бота
token = os.getenv("BOT_TOKEN")
logging.info(token)
bot = Bot(token=token)
dp = Dispatcher()


@dp.message()

@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Hello!")


# Запуск процесса полинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import os
import dotenv
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config

# Включаем логгирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Получим переменные окружения

dotenv.load_dotenv()
# Объект бота
token = os.getenv("BOT_TOKEN")
logging.info(token)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message(Command("dice"))
async def cmd_dice(message: types.Message, bot: Bot):
    await bot.send_dice(1601602567, emoji=DiceEmoji.DICE)


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Hello!")


@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, my_list: list[int]):
    my_list.append(7)
    await message.answer("Добавлено число 7")


@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message, my_list: list[int]):
    await message.answer(f"Ваш список {my_list}")


@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")


# Запуск процесса полинга новых апдейтов
async def main():
    # Иногда при старте бота требуется передать одно или несколько
    # дополнительных значений
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    await dp.start_polling(bot, my_list=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())

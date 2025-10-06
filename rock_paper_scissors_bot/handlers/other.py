from aiogram import Router
from aiogram.types import Message

from lexicon import LEXICON_RU

other_router = Router()

# Создаём хэндлер для обработки сообщений, которые не попали
# в другие хэндлеры


@other_router.message()
async def other_message(message: Message):
    await message.answer(text=LEXICON_RU["other_answer"])

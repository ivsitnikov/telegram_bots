from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU


router = Router()


# Этот хендлер срабатывает на команду /start
@router.message(CommandStart())
async def process_comand_start(message: Message):
    await message.answer(text=LEXICON_RU["/start"])


# Этот хендлер срабатывает на команду /help
@router.message(Command(commands="help"))
async def process_comand_help(message: Message):
    await message.answer(text=LEXICON_RU["/help"])

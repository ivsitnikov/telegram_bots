from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon import LEXICON_RU, BUTTON
from services import get_winner, get_bot_choice
from keyboards import game_kb, yes_no_kb, generate_inline_keyboard


user_router = Router()


@user_router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON_RU["/start"], reply_markup=yes_no_kb)


@user_router.message(Command(commands="help"))
async def process_help(message: Message):
    await message.answer(text=LEXICON_RU["/help"], reply_markup=yes_no_kb)


@user_router.message(Command(commands="generate_inline_kb"))
async def process_generate_inline_kb(message: Message):
    # keyboard = generate_inline_keyboard(2, **BUTTON)
    keyboard = generate_inline_keyboard(2, "but_1", "but_3", "but_7")
    await message.answer(text=LEXICON_RU["/generate_inline_kb"], reply_markup=keyboard)


@user_router.message(F.text == LEXICON_RU["yes_button"])
async def process_yes_button(message: Message):
    await message.answer(text=LEXICON_RU["yes"], reply_markup=game_kb)


@user_router.message(F.text == LEXICON_RU["no_button"])
async def process_no_button(message: Message):
    await message.answer(text=LEXICON_RU["no"])


@user_router.message(
    F.text.in_([LEXICON_RU["rock"], LEXICON_RU["papper"], LEXICON_RU["scissors"]])
)
async def process_game(message: Message):
    bot_choice: str = get_bot_choice()
    await message.answer(text=f"{LEXICON_RU['bot_choice']} - {LEXICON_RU[bot_choice]}")
    user_answer: str = message.text
    winner = get_winner(user_answer, bot_choice)
    if winner == "user_won":
        message_effect_id = "5046509860389126442"
    else:
        message_effect_id = None
    await message.answer(
        text=LEXICON_RU[winner],
        message_effect_id=message_effect_id,
        reply_markup=yes_no_kb,
    )

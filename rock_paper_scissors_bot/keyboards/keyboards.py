from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON_RU


# ----- Создаём клавиатуру для принятия решения о начале игры
# Создаём кнопки для принятия решения
yes_btn = KeyboardButton(text=LEXICON_RU["yes_button"])
no_btn = KeyboardButton(text=LEXICON_RU["no_button"])


# Инициализация билдера для создания клавиатуры с кнопками Давай и Не хочу
kb_builder_yes_no = ReplyKeyboardBuilder()
kb_builder_yes_no.row(yes_btn, no_btn, width=2)

yes_no_kb: ReplyKeyboardMarkup = kb_builder_yes_no.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)

# ----- Создаём клавиауру для игры
# Создаём игровые кнопки
rock_btn = KeyboardButton(text=LEXICON_RU["rock"])
papper_btn = KeyboardButton(text=LEXICON_RU["papper"])
scissors_btn = KeyboardButton(text=LEXICON_RU["scissors"])

game_kb = ReplyKeyboardMarkup(
    keyboard=[[rock_btn], [papper_btn], [scissors_btn]], resize_keyboard=True
)

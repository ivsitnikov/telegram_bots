from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utilites import InlineKeyboardBuilder
from lexicon import LEXICON_RU


def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    builder_kb = InlineKeyboardBuilder()
    builder_kb.row(
        *[
            InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button,
            )
            for button in buttons
        ]
    )
    return builder_kb.as_markup()

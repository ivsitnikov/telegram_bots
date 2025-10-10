from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon import BUTTON, LEXICON_INLINE_BUTTON


def generate_inline_keyboard(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON_INLINE_BUTTON[button]
                    if button in LEXICON_INLINE_BUTTON
                    else button,
                    callback_data=button,
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    # Распаковываем список с кнопками с аргументом width
    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()

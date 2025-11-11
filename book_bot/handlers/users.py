from copy import deepcopy
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards import (
    create_edit_keyboard,
    create_bookmarks_keyboard,
    create_pagination_kb,
)
from filters import IsDigitCallbackData, IsDelBookmarkCallbackData
from lexicon import LEXICON_RU
from database import db_init


user_router = Router()


# Этот хэндлер будет срабатывать при введении команды /start
# и добавлять в базу пользователя, если его там еще нет
@user_router.message(CommandStart())
async def process_command_start(message: Message, db: dict):
    await message.answer(LEXICON_RU[message.text])
    if message.from_user.id not in db:
        db["users"][message.from_user.id] = deepcopy(db.get("user_template"))


# Этот хендлер будет срабатывать на отправку пользователем команды /help
@user_router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(LEXICON_RU[message.text])


# Этот хэндлер будет срабатывать на команду /beginnfing
@user_router.message(Command(commands="beginning"))
async def process_command_begining(message: Message, book: dict, db: dict):
    db["users"][message.from_user.id]["page"] = 1
    text = book[1]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            "backward",
            f"1/{len(book)}",
            "forward",
        ),
    )


# Этот хэндлер будет срабатывать на команду /continue
@user_router.message(Command(commands="continue"))
async def process_command_continue(message: Message, book: dict, db: dict):
    text = book[db["users"][message.from_user.id]["page"]]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            "backward",
            f"{db['users'][message.from_user.id]['page']}/{len(book)}",
            "forward",
        ),
    )


# Этот хэндлер будет срабатывать на команду /bookmarks
@user_router.message(Command(commands="bookmarks"))
async def process_command_continue(message: Message, book: dict, db: dict):
    if db["users"][message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_bookmarks_keyboard(
                *db["users"][message.from_user.id]["bookmarks"],
                book=book,
            ),
        )
    else:
        await message.answer(
            text=LEXICON_RU["no_bookmarks"],
        )


# Этот хэндлер будет срабатывать на нажатие кнопки "вперед"
@user_router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery, book: dict, db: dict):
    current_page = db["users"][callback.from_user.id]["page"]
    if current_page < len(book):
        db["users"][callback.from_user.id]["page"] += 1
        text = book[current_page + 1]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                "backward",
                f"{current_page}/{len(book)}",
                "forward",
            ),
        )
    await callback.answer()


# Этот хэндлер будет срабатывать при нажатии на кнопку "назад"
@user_router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery, book: dict, db: dict):
    current_page = db["users"][callback.from_user.id]["page"]
    if current_page > 1:
        db["users"][callback.from_user.id]["page"] -= 1
        text = book[current_page - 1]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                "backward",
                f"{db['users'][callback.from_user.id]['page']}/{len(book)}",
                "forward",
            ),
        )
    else:
        await callback.answer()


# Этот хэндлер будет срабатывать при нажатии на инлайн кнопку с номером/
# колличеством страниц для добавления страницы в закладку
@user_router.callback_query(
    lambda x: "/" in x.data and x.data.replace("/", "").isdigit()
)
async def process_page_press(callback: CallbackQuery, db: dict):
    db["users"][callback.from_user.id]["bookmarks"].add(
        db["users"][callback.from_user.id]["page"]
    )
    await callback.answer("Страница добавлена в закладки")


# Этот хэндлер будет срабатывать при нажатии на кнопку из списка закладок
@user_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, book: dict, db: dict):
    text = book[int(callback.data)]
    db["users"][callback.from_user.id]["page"] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            "backward",
            f"{db['users'][callback.from_user.id]['page']}/{len(book)}",
            "forward",
        ),
    )


# Этот хэндлер будет срабатывать на нажатие на инлайн кнопку "редактировать"
# под списком закладок


@user_router.callback_query(F.data == "edit_bookmarks")
async def proccess_edit_press(callback: CallbackQuery, db: dict, book: dict):
    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard(
            *db["users"][callback.from_user.id]["bookmarks"], book=book
        ),
    )


# Этот хэндлер будет срабатывать при нажатии на инлайн кнопку 'отмена' под списком
# закладок
@user_router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU["cancel_text"],
    )


# Этот хэндлер будет срабатывать при нажатии на инлайн кнопку "редактировать"
# под списком закладок к удалению
@user_router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmarks_press(callback: CallbackQuery, book: dict, db: dict):
    db["users"][callback.from_user.id]["bookmarks"].remove(int(callback.data[:-3]))
    if db["users"][callback.from_user.id]["bookmarks"]:
        await callback.message.edit_text(
            text=LEXICON_RU["/bookmarks"],
            reply_markup=create_edit_keyboard(
                *db["users"][callback.from_user.id]["bookmarks"], book=book
            ),
        )
    else:
        await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])

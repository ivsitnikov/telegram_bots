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


# Добавим обработку ошибок и валидацию
async def validate_user_exists(user_id: int, db: dict) -> bool:
    """Проверяет существование пользователя в БД"""
    return user_id in db.get("users", {})


async def get_user_page(user_id: int, db: dict) -> int:
    """Безопасно получает текущую страницу пользователя"""
    return db["users"].get(user_id, {}).get("page", 1)


async def get_user_bookmarks(user_id: int, db: dict) -> set:
    """Безопасно получает закладки пользователя"""
    return db["users"].get(user_id, {}).get("bookmarks", set())


# Команда /start
@user_router.message(CommandStart())
async def process_command_start(message: Message, db: dict):
    await message.answer(LEXICON_RU[message.text])

    # Инициализация пользователя
    if not await validate_user_exists(message.from_user.id, db):
        db["users"][message.from_user.id] = deepcopy(db.get("user_template", {}))
        # Добавляем базовые поля если их нет в шаблоне
        db["users"][message.from_user.id].setdefault("page", 1)
        db["users"][message.from_user.id].setdefault("bookmarks", set())


# Команда /help
@user_router.message(Command(commands="help"))
async def process_command_help(message: Message):
    await message.answer(LEXICON_RU[message.text])


# Команда /beginning
@user_router.message(Command(commands="beginning"))
async def process_command_beginning(message: Message, book: dict, db: dict):
    if not await validate_user_exists(message.from_user.id, db):
        await process_command_start(message, db)
        return

    db["users"][message.from_user.id]["page"] = 1
    text = book.get(1, LEXICON_RU.get("page_not_found", "Страница не найдена"))

    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            "backward",
            f"1/{len(book)}",
            "forward",
        ),
    )


# Команда /continue
@user_router.message(Command(commands="continue"))
async def process_command_continue(message: Message, book: dict, db: dict):
    if not await validate_user_exists(message.from_user.id, db):
        await process_command_start(message, db)
        return

    current_page = await get_user_page(message.from_user.id, db)
    text = book.get(
        current_page, LEXICON_RU.get("page_not_found", "Страница не найдена")
    )

    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            "backward",
            f"{current_page}/{len(book)}",
            "forward",
        ),
    )


# Команда /bookmarks
@user_router.message(Command(commands="bookmarks"))
async def process_command_bookmarks(message: Message, book: dict, db: dict):
    if not await validate_user_exists(message.from_user.id, db):
        await process_command_start(message, db)
        return

    bookmarks = await get_user_bookmarks(message.from_user.id, db)

    if bookmarks:
        await message.answer(
            text=LEXICON_RU[message.text],
            reply_markup=create_bookmarks_keyboard(
                *bookmarks,
                book=book,
            ),
        )
    else:
        await message.answer(text=LEXICON_RU["no_bookmarks"])


# Навигация вперед
@user_router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery, book: dict, db: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    current_page = await get_user_page(callback.from_user.id, db)

    if current_page < len(book):
        new_page = current_page + 1
        db["users"][callback.from_user.id]["page"] = new_page
        text = book.get(
            new_page, LEXICON_RU.get("page_not_found", "Страница не найдена")
        )

        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                "backward",
                f"{new_page}/{len(book)}",
                "forward",
            ),
        )
    else:
        await callback.answer("Вы достигли конца книги")

    await callback.answer()


# Навигация назад
@user_router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery, book: dict, db: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    current_page = await get_user_page(callback.from_user.id, db)

    if current_page > 1:
        new_page = current_page - 1
        db["users"][callback.from_user.id]["page"] = new_page
        text = book.get(
            new_page, LEXICON_RU.get("page_not_found", "Страница не найдена")
        )

        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                "backward",
                f"{new_page}/{len(book)}",
                "forward",
            ),
        )
    else:
        await callback.answer("Вы на первой странице")

    await callback.answer()


# Добавление закладки
@user_router.callback_query(
    lambda x: "/" in x.data and x.data.replace("/", "").isdigit()
)
async def process_page_press(callback: CallbackQuery, db: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    current_page = await get_user_page(callback.from_user.id, db)
    bookmarks = await get_user_bookmarks(callback.from_user.id, db)

    if current_page not in bookmarks:
        db["users"][callback.from_user.id]["bookmarks"].add(current_page)
        await callback.answer("Страница добавлена в закладки")
    else:
        await callback.answer("Страница уже в закладках")


# Переход к закладке
@user_router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery, book: dict, db: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    try:
        page_num = int(callback.data)
        if 1 <= page_num <= len(book):
            db["users"][callback.from_user.id]["page"] = page_num
            text = book.get(
                page_num, LEXICON_RU.get("page_not_found", "Страница не найдена")
            )

            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_kb(
                    "backward",
                    f"{page_num}/{len(book)}",
                    "forward",
                ),
            )
        else:
            await callback.answer("Неверный номер страницы")
    except ValueError:
        await callback.answer("Ошибка: неверный формат данных")

    await callback.answer()


# Редактирование закладок
@user_router.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery, db: dict, book: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    bookmarks = await get_user_bookmarks(callback.from_user.id, db)

    await callback.message.edit_text(
        text=LEXICON_RU[callback.data],
        reply_markup=create_edit_keyboard(*bookmarks, book=book),
    )


# Отмена редактирования
@user_router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["cancel_text"])


# Удаление закладки
@user_router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmarks_press(callback: CallbackQuery, book: dict, db: dict):
    if not await validate_user_exists(callback.from_user.id, db):
        await callback.answer("Ошибка: пользователь не найден")
        return

    try:
        page_to_remove = int(callback.data[:-3])
        bookmarks = await get_user_bookmarks(callback.from_user.id, db)

        if page_to_remove in bookmarks:
            db["users"][callback.from_user.id]["bookmarks"].remove(page_to_remove)

            # Обновляем клавиатуру
            updated_bookmarks = await get_user_bookmarks(callback.from_user.id, db)
            if updated_bookmarks:
                await callback.message.edit_text(
                    text=LEXICON_RU["/bookmarks"],
                    reply_markup=create_edit_keyboard(*updated_bookmarks, book=book),
                )
            else:
                await callback.message.edit_text(text=LEXICON_RU["no_bookmarks"])
        else:
            await callback.answer("Закладка не найдена")
    except ValueError:
        await callback.answer("Ошибка: неверный формат данных")

    await callback.answer()


# Добавим обработку неизвестных команд
@user_router.message()
async def process_unknown_command(message: Message):
    await message.answer(LEXICON_RU.get("unknown_command", "Неизвестная команда"))

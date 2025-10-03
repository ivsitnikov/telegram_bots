import logging
from aiogram.enums import PollType
from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
    KeyboardButtonPollType,
    PollAnswer,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestUsers,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Инициализация диспетчера")
dp = Dispatcher()

logger.info("Загрузка кофигурационных данных")
config = Config.load()
logger.info(f"{config.telegram.bot_token.get_secret_value()}")

logger.info("Инициализация объекта бота")
bot = Bot(token=config.telegram.bot_token.get_secret_value())

logger.info("Создание клавиатуры")

# Создание билдера
kb_builder = ReplyKeyboardBuilder()

# Созлание кнопок
# Создание кнопок с помощью list comprehantions
# keyboard: list[KeyboardButton] = [KeyboardButton(text=str(i)) for i in range(1, 8)]
# kb_builder.row(*keyboard, width=3)
# my_keyboard = kb_builder.as_markup(resize_keyboard=True)

# Еще один способ создания кнопок с помощью list comprehantions
# и размещение их в интерфейсе телеграмм бота
keyboard: list[list[KeyboardButton]] = [
    [KeyboardButton(text=str(i)) for i in range(1, 4)],
    [KeyboardButton(text=str(i)) for i in range(4, 7)],
    #    [KeyboardButton(text=str(i)) for i in range(7, 9)],
]
keyboard.append([KeyboardButton(text="7")])
my_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=keyboard, resize_keyboard=True
)
# Еще один пример создания клавиатуры с помощью list comprehantions

# Кнопка выбора пользователя для отправки в чат личного сообщения
# request_user_btn = KeyboardButton(
#    text="Выбор пользователя",
#    request_user=KeyboardButtonRequestUser(request_id=42, user_is_premium=False),
# )
# Кнопка выбора группы пользователей для отправки сообщения
# request_users_btn = KeyboardButton(
#    text="Выбор группы пользователей",
#    request_users=KeyboardButtonRequestUsers(
#        request_id=77, user_is_premium=False, max_quantity=3
#    ),
# )
# Кнопка выбора чата для отправки сообщения
# request_chat_btn = KeyboardButton(
#    text="Выбор чата с пользователями",
#    request_chat=KeyboardButtonRequestChat(
#        request_id=1408, chat_is_channel=False, chat_is_forum=False
#    ),
# )
# Кнопка отправки контакта пользователя
# button_1 = KeyboardButton(text="Отправить контакт", request_contact=True)
# Кнопка для отправки геопозиции пользователя
# button_2 = KeyboardButton(text="Отправить геолокацию", request_location=True)
# Просто кнопка - она отправляет текст в чат
# button_3 = KeyboardButton(text="кнопка_3")
# Кнопка для создания опроса/викторины в чат
# poll_quiz_btn = KeyboardButton(
#    text="Создание опроса", request_poll=KeyboardButtonPollType()
# )
# Кнопка для создания опроса
# poll_btn = KeyboardButton(
#    text="Создание опроса", request_poll=KeyboardButtonPollType(type=PollType.REGULAR)
# )
# Кнопка для создания викторины
# quiz_btn = KeyboardButton(
#    text="Создание викторины", request_poll=KeyboardButtonPollType(type=PollType.QUIZ)
# )
# Кнопка для создания веб-интерфейса телеграмм бота
# web_app_btn = KeyboardButton(
#    text="WebApp", web_app=WebAppInfo(url="https://stepik.org/")
# )

# Добавление кнопок в билдер
# kb_builder.row(web_app_btn, width=1)


# Инициализация объекта клавиатуры
# keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)


# Хендлер срабатывающий на команду старт
@dp.message(CommandStart())
async def process_comand_start(message: Message):
    await message.answer(
        text="Начало работы бота. Демонстрация работы клавиатуры",
        reply_markup=my_keyboard,
    )


# Этот хэндлер будет срабатывать на команду /web_app
# @dp.message(Command(commands="web_app"))
# async def process_command_web_app(message: Message):
#    await message.answer(
#        text="Эксперементируем со специальными кнопками", reply_markup=keyboard
#    )


# Этот хэндлер будет срабатывать на выбор пользователя из списка
# @dp.message(F.user_shared)
# async def process_user_shared(message: Message):
#    logger.info(
#        f"Выбор пользователя из списка {message.model_dump_json(indent=4, exclude_none=True)}"
#    )


# Этот хэндлер будет срабатывать на выбор пользователей из списка
# @dp.message(F.users_shared)
# async def process_users_shared(message: Message):
#    logger.info(
#        f"Выбор пользователя из списка {message.model_dump_json(indent=4, exclude_none=True)}"
#    )


# Этот хэндлер будет срабатывать на выбор чата из списка
# @dp.message(F.chat_shared)
# async def process_chat_shared(message: Message):
#    logger.info(
#        f"Выбор пользователя из списка {message.model_dump_json(indent=4, exclude_none=True)}"
#    )


# Этот хэндлер будет срабатывать на отправку викторины
# @dp.message(F.poll.type == PollType.QUIZ)
# async def process_poll_quiz(message: Message):
#    await message.answer_poll(
#                question=message.poll.question
#                options=[opt.text for opt in message.poll.options],
#
#        is_anonymous=False,
#        type=message.poll.type,
#        correct_option_id=message.poll.correct_option_id,
#        explanationf=message.poll.explanation,
#        explanation_entities=message.poll.explanation_entities,
#        message_effect_id="5104841245755180586",
#    )
#    logger.info("Викторина отправлена в чат")


# Этот хэндлер будет срабатывать на отправку опроса
# @dp.message(F.poll.type == PollType.REGULAR)
# async def process_poll_regular(message: Message):
#    await message.answer_poll(
#        question=message.poll.question,
#        options=[opt.text for opt in message.poll.options],
#        is_anonymous=False,
#        type=message.poll.type,
#        allows_multiple_answers=message.poll.allows_multiple_answers,
#        message_effect_id="5107584321108051014",
#    )
#    logger.info("Опрос отправлен в чат")


# Этот хэндлер будет срабатвать на отправку опроса ответа опросе/викторине
# @dp.poll_answer()
# async def process_answer_poll(poll_answer: PollAnswer):
#    logger.info(
#        f"Ответ пользователя {poll_answer.model_dump_json(indent=4, exclude_none=True)}"
#    )


# Создаем хэндлер, который будет срабатывать на отправку опроса/викторины

# @dp.message(F.poll)
# async def process_poll(message: Message):
#    print(message.model_dump_json(indent=4, exclude_none=True))

# Этот хэндлер будет срабатывать при отправке контакта пользователя
# @dp.message(F.contact)
# async def process_key_2(message: Message):
#    await message.reply(text=f"Ваш телефон {message.contact.phone_number}")

# Этот хэндлер будет срабатывать на отправку геолокации пользователя
# @dp.message(F.location)
# async def process_message(message: Message):
#    await message.reply(
#        text=f"Ваша геолокация {message.location.latitude} {message.location.longitude}"
#    )


if __name__ == "__main__":
    logger.info("Старт бота")
    dp.run_polling(bot)

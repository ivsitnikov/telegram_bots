from aiogram import Bot
from aiogram.types import BotCommand
from lexicon import COMMANDS_RU


async def set_menu(bot: Bot):
    menu: list[BotCommand] = [
        BotCommand(command=command, description=description)
        for command, description in COMMANDS_RU.items()
    ]
    await bot.set_my_commands(menu)

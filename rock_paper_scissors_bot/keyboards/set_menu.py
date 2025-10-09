from aiogram import Bot
from aiogram.types import BotCommand

from lexicon import LEXICON_RU_COMMANDS


async def set_main_menu(bot: Bot):
    main_menu = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_RU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu)

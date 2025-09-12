import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
import logging
from config_reader import config
import dotenv


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
logger.info(config.bot_token)
bot = Bot(token=config.bot_token.get_secret_value())

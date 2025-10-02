from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
import logging
from config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = Config.load()

dp = Dispatcher()
logger.info(config.telegram.bot_token.get_secret_value())
# bot = Bot(tokn=config.bot_token.get_secret_value())

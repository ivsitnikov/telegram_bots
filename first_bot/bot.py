import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логгирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO) 
# Объект бота
bot = Bot(token=...) 
dp = Dispatcher()

if __name__ == "__main__":
    asyncio.run(main())
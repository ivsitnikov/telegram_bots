# Данный код для бота демонстрирует работу с сообщениями:
- текстом (форматирование, html и markdown parser,);
- entities;
- показывает сохранение дефолтных настроек;
- работу с командами и их аргументами;
- Диплинки;
- Предпросмотр ссылок.

**В коде используются инструменты библиотеки aiogram:**
1. импорт из aiogram фильтр F
2. импорт из aiogram.filters фильтра Command
3. from aiogram.enums import ParseMode
4. from aiogram.client.default import DefaultBotProperties
5. from aiogram import html
6. from aiogram.utils.formatting import Text,
    Bold, as_list, as_marked_section, as_key_value, HashTag

https://mastergroosha.github.io/aiogram-3-guide/messages/
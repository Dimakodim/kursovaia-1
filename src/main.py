import asyncio
import logging
import sys
import sqlite3

from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from aiogram.client.session.aiohttp import AiohttpSession

from modules.start.start_module import start_router
from modules.create.create_module import create_router
from modules.join.join_module import join_router
from modules.list.list_module import list_router
from modules.show_queue.show_queue_module import show_queue_router

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "8748414894:AAFSJ-l21rAvWGpysCLhktEZjoQACFAGsG8"

# All handlers should be attached to the Router (or Dispatcher)
PROXY_URL = 'http://127.0.0.1:12334'

dp = Dispatcher()
conn = sqlite3.connect('src/data.db', check_same_thread=False)
cursor = conn.cursor()

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    
    session = AiohttpSession(proxy=PROXY_URL)
    # bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(start_router)
    dp.include_router(create_router)
    dp.include_router(join_router)
    dp.include_router(list_router)
    dp.include_router(show_queue_router)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
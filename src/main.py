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

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "8748414894:AAGEbVkb1vkWTMoY-ifzOnn-Y2S1W7IHOb0"

# All handlers should be attached to the Router (or Dispatcher)
PROXY_URL = 'http://127.0.0.1:12334'

dp = Dispatcher()
conn = sqlite3.connect('src/data.db', check_same_thread=False)
cursor = conn.cursor()

""" @dp.message(Command("create"))
async def create_queue(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    
    queue_name = command.args

    cursor.execute(f'SELECT id FROM users WHERE user_id = {message.from_user.id}')
    author_id = cursor.fetchall()[0][0]

    cursor.execute("INSERT INTO queue (name, author_id) VALUES (?, ?)", (queue_name, author_id))
    conn.commit()
    await message.answer(
        f"Создана очередь: {queue_name}"
    )   """      

@dp.message(Command("list"))
async def print_list(
        message: Message
):
    cursor.execute(f'SELECT id FROM users WHERE user_id = {message.from_user.id}')
    author_id = cursor.fetchall()[0][0]

    cursor.execute(f'SELECT name FROM queue WHERE author_id = {author_id}')
    conn.commit()
    await message.answer(
        f"Очереди: {cursor.fetchall()}"
    ) 

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(start_router)
    dp.include_router(create_router)
    dp.include_router(join_router)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
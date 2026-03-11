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

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "8748414894:AAH7Kej4ainQsEj7NWJGUUN0zbgXyHIHOJM"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
conn = sqlite3.connect('src/data.db', check_same_thread=False)
cursor = conn.cursor()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    try:
        cursor.execute(f"INSERT INTO users (user_id) VALUES ({message.from_user.id})")
        conn.commit()
        await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
    except sqlite3.IntegrityError:
        await message.answer("Уже здоровались")

@dp.message(Command("create"))
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
    )        

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
    


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
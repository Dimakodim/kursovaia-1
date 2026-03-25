import aiogram
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from .start_keyboard import *
from .start_db import *

start_router = Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}!\nЯ бот для очередей!', reply_markup=start_kb())



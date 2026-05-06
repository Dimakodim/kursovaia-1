import aiogram
import asyncio
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from ..start import start_keyboard
from .list_keyboard import *
from .list_db import *

list_router = Router()

class ListState(StatesGroup):
    id_input = State()
    loading = State()

@list_router.message(Command("list"), StateFilter(None))
@list_router.message(F.text.contains("Мои очереди"), StateFilter(None))
async def command_list_handler(message: Message, state: FSMContext) -> None:
    queue_list = showList(message.from_user.id)
    text = 'Список очередей:\n'
    for i in queue_list:
        text += f'{i[0]}) {i[1]}\n'
    await message.answer(text, reply_markup=list_kb([i[0] for i in queue_list]), parse_mode=None)
    await state.set_state(ListState.id_input)

@list_router.message(F.text.contains('Отмена'), StateFilter(ListState.id_input))
async def command_return_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(ListState.loading)
    msg = await message.answer(f'Отмена...', reply_markup=None)

    await asyncio.sleep(3)
    await msg.delete()

    await state.clear()
    await message.answer(f'Успешно!', reply_markup=start_keyboard.start_kb())
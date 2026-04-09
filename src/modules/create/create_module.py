import aiogram
import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .create_keyboard import *
from .create_db import *
from ..start import start_keyboard
import re

create_router = Router()

class CreateState(StatesGroup):
    choosing_queue_name = State()
    loading = State()

@create_router.message(Command("create"), StateFilter(None))
@create_router.message(F.text.regexp(r"создать", flags=re.IGNORECASE), StateFilter(None))
async def command_create_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите название очереди:', reply_markup=create_kb())

    await state.set_state(CreateState.choosing_queue_name)

@create_router.message(F.text.contains('Отмена ❌'), StateFilter(CreateState.choosing_queue_name))
async def command_return_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CreateState.loading)
    msg = await message.answer(f'Отмена создания...', reply_markup=None)

    await asyncio.sleep(3)
    await msg.delete()

    await state.clear()
    await message.answer(f'Успешно!', reply_markup=start_keyboard.start_kb())

@create_router.message(StateFilter(CreateState.choosing_queue_name))
async def command_choose_handler(message: Message, state: FSMContext) -> None:
    if message.text:
        if len(message.text) <= 255:
            await state.set_state(CreateState.loading)
            code = createQueue(message.text, message.from_user.id)
            if code:
                await message.answer(f"Очередь создана, код доступа: <b><tg-spoiler>{code}</tg-spoiler></b>", parse_mode="HTML",
                                    reply_markup=start_keyboard.start_kb())
            else:
                await message.answer("❌ Ошибка 0x0029471. Обратитесь к создателю бота!! ❌",
                                    reply_markup=start_keyboard.start_kb())
            await state.clear()
        else:
            await message.answer("❌ Название очереди не может быть больше 255 символов!! ❌")
    else:
        await message.answer("❌ Введите название очереди!! ❌")
        

import aiogram
import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .join_keyboard import *
from .join_db import *
from ..start import start_keyboard


join_router = Router()

class JoinState(StatesGroup):
    code_input = State()
    loading = State()

@join_router.message(Command("join"), StateFilter(None))
@join_router.message(F.text.contains("Присоедениться к очереди 🗝️"), StateFilter(None))
async def command_join_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f'Введите код приглашения:', reply_markup=join_kb())

    await state.set_state(JoinState.code_input)

@join_router.message(F.text.contains('Отмена ❌'), StateFilter(JoinState.code_input))
async def command_return_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(JoinState.loading)
    msg = await message.answer(f'Отмена...', reply_markup=None)

    await asyncio.sleep(3)
    await msg.delete()

    await state.clear()
    await message.answer(f'Успешно!', reply_markup=start_keyboard.start_kb())

@join_router.message(StateFilter(JoinState.code_input))
async def code_input_handler(message: Message, state: FSMContext) -> None:
    if message.text:
        try:
            await state.set_state(JoinState.loading)
            code = int(message.text)
            joinQueue(message.from_user.id, code)
            await state.clear()
            await message.answer("Вы успешно присоелинились к очереди!", reply_markup=start_keyboard.start_kb())
        except ValueError:
            await message.answer("❌ Введите шестизначное число!! ❌")
            await state.set_state(JoinState.code_input)
        except UnknownUserError:
            await message.answer("❌ Ошибка индефикации!! Вы прописывали команду /start? ❌", reply_markup=start_keyboard.start_kb())
            await state.clear()
        except InvalidCodeError:
            await message.answer("❌ Неверный код доступа!! ❌")
            await state.set_state(JoinState.code_input)
        except RepeatJoinError:
            await message.answer("❌ Вы пытаетесь войти в очередь, в которой состоите!! Серьезно? ❌", reply_markup=start_keyboard.start_kb())
            await state.clear()
    else:
        await message.answer("❌ Введите код доступа!! ❌")
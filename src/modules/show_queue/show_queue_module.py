import aiogram
from aiogram import Router, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from .show_queue_keyboard import *
from .show_queue_db import *
from ..list.list_module import ListState
from aiogram.utils.formatting import Text, BlockQuote, Code, TextLink
from ..start import start_keyboard
import json

show_queue_router = Router()

@show_queue_router.message(StateFilter(ListState.id_input))
async def id_queue_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    try:
        queue = showQueue(message.from_user.id, message.text)
        if len(queue) == 0:
            await message.answer("Ошибка! Такой очереди не существует!")
        else:
            list_queue = json.loads(queue[0][4])
            text_queue = []
            for i in range(len(list_queue)):
                you_text = ''
                user_id = getTgIdById(list_queue[i])
                if user_id:
                    if user_id[0] == message.from_user.id: you_text = ' - вы'
                    chat = await bot.get_chat(chat_id=user_id[0])
                    text_queue.append(BlockQuote(f'{i+1}) {chat.full_name}'+you_text)+"\n")
            admin_id = getTgIdById(queue[0][2])
            admin_text = ''
            if admin_id:
                chat = await bot.get_chat(chat_id=admin_id[0])
                admin_text = ['\n\nАдминистратор очереди: ', Code(chat.full_name)]
            content = Text(Code(queue[0][1]), '\n\n', *text_queue, *admin_text)
            await message.answer(**content.as_kwargs(), reply_markup=show_queue_kb())
            await state.clear()

    except ValueError:
        await message.answer("Введите корректный айди очереди")

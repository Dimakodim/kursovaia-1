import aiogram
from aiogram import Router, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from .show_queue_keyboard import *
from .show_queue_db import *
from ..list.list_module import ListState
from aiogram.utils.formatting import Text, BlockQuote, Code, TextLink
from ..start import start_keyboard
from ..show_queue.show_queue_keyboard import QueueCallback
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
            kb = show_queue_kb(queue[0][0])
            admin_id = getTgIdById(queue[0][2])
            admin_text = ''
            if admin_id:
                chat = await bot.get_chat(chat_id=admin_id[0])
                admin_text = ['\n\nАдминистратор очереди: ', Code(chat.full_name)]
                if admin_id[0] == message.from_user.id:
                    kb = show_queue_kb(queue[0][0], True)
            content = Text(Code(queue[0][1]), '\n\n', *text_queue, *admin_text)
            await message.answer(**content.as_kwargs(), reply_markup=kb)
            await state.clear()

    except ValueError:
        await message.answer("Введите корректный айди очереди")

@show_queue_router.callback_query(QueueCallback.filter())
async def handle_callback(
    query: CallbackQuery, 
    callback_data: QueueCallback,
    bot: Bot
):
    await query.answer()
    match callback_data.button:
        case "btn_1":
            putUserToEnd(query.from_user.id, callback_data.id)
            content, kb = await updateQueue(query.from_user.id, callback_data.id, bot)
            await query.message.edit_text(**content.as_kwargs())
            await query.message.edit_reply_markup(reply_markup=kb)
        case "btn_2":
            putUserToEnd(query.from_user.id, callback_data.id)
            content, kb = await updateQueue(query.from_user.id, callback_data.id, bot)
            await query.message.edit_text(**content.as_kwargs())
            await query.message.edit_reply_markup(reply_markup=kb)
        case "btn_3":
            skipOne(query.from_user.id, callback_data.id)
            content, kb = await updateQueue(query.from_user.id, callback_data.id, bot)
            await query.message.edit_text(**content.as_kwargs())
            await query.message.edit_reply_markup(reply_markup=kb)
        case "btn_4":
            leaveQueue(query.from_user.id, callback_data.id)
            await query.message.delete()
        case "btn_5":
            pass
        case "btn_6":
            pass
        case _:
            pass

async def updateQueue(user_ids, id, bot):
    queue = showQueue(user_ids, id)
    list_queue = json.loads(queue[0][4])
    text_queue = []
    for i in range(len(list_queue)):
        you_text = ''
        user_id = getTgIdById(list_queue[i])
        if user_id:
            if user_id[0] == user_ids: you_text = ' - вы'
            chat = await bot.get_chat(chat_id=user_id[0])
            text_queue.append(BlockQuote(f'{i+1}) {chat.full_name}'+you_text)+"\n")
    kb = show_queue_kb(queue[0][0])
    admin_id = getTgIdById(queue[0][2])
    admin_text = ''
    if admin_id:
        chat = await bot.get_chat(chat_id=admin_id[0])
        admin_text = ['\n\nАдминистратор очереди: ', Code(chat.full_name)]
        if admin_id[0] == user_ids:
            kb = show_queue_kb(queue[0][0], True)
    content = Text(Code(queue[0][1]), '\n\n', *text_queue, *admin_text)
    return content, kb
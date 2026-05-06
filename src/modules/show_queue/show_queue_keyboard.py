from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def show_queue_kb():
    kb_list = [
    [InlineKeyboardButton(text="Я сдал", callback_data="btn_1")],
    [InlineKeyboardButton(text="В конец очереди", callback_data="btn_2"), InlineKeyboardButton(text="Пропустить одного", callback_data="btn_3")],
    [InlineKeyboardButton(text="Покинуть очередь", callback_data="btn_4")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
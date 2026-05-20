from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def show_queue_kb(is_admin = False):
    kb_list = [
    [InlineKeyboardButton(text="Я сдал", callback_data="btn_1")],
    [InlineKeyboardButton(text="В конец очереди", callback_data="btn_2"), InlineKeyboardButton(text="Пропустить одного", callback_data="btn_3")],
    [InlineKeyboardButton(text="Покинуть очередь", callback_data="btn_4")]]
    if is_admin:
        kb_list.append([InlineKeyboardButton(text="Удалить человека", callback_data="btn_5",style="danger"), InlineKeyboardButton(text="Удалить очередь", callback_data="btn_6",style="danger")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
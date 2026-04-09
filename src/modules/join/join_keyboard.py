from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def join_kb():
    kb_list = [[KeyboardButton(text="Отмена ❌")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

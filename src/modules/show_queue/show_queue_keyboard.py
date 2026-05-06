from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def show_queue_kb():
    kb_list = [[KeyboardButton(text="show_queue")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

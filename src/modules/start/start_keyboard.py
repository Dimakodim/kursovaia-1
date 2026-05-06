from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def start_kb():
    kb_list = [
        [KeyboardButton(text="Мои очереди 📋"), KeyboardButton(text="Создать очередь ➕")],
        [KeyboardButton(text="Присоединиться к очереди 🗝️")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
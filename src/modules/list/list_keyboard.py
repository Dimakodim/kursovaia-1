from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def list_kb(queue_list = []):
    kb_list = []
    for i in range(0, len(queue_list)):
        if i%2 == 0:
            kb_list = [[KeyboardButton(text=str(queue_list[i]))]] + kb_list
        else:
            kb_list[0].append(KeyboardButton(text=str(queue_list[i])))
    kb_list.reverse()
    kb_list.append([KeyboardButton(text="Отмена")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

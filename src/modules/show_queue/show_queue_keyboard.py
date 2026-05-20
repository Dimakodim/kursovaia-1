from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class QueueCallback(CallbackData, prefix = "queue"):
    button: str
    id: int

class DeleteCallback(CallbackData, prefix = "delete"):
    queue_id: int
    id: int

def show_queue_kb(id, is_admin = False):
    kb_list = [
    [InlineKeyboardButton(text="Я сдал", callback_data=QueueCallback(button="btn_1", id=id).pack())],
    [InlineKeyboardButton(text="В конец очереди", callback_data=QueueCallback(button="btn_2", id=id).pack()),
     InlineKeyboardButton(text="Пропустить одного", callback_data=QueueCallback(button="btn_3", id=id).pack())],
    [InlineKeyboardButton(text="Покинуть очередь", callback_data=QueueCallback(button="btn_4", id=id).pack())]]
    if is_admin:
        kb_list.append([InlineKeyboardButton(text="Удалить человека", callback_data=QueueCallback(button="btn_5", id=id).pack(),style="danger"), 
                        InlineKeyboardButton(text="Удалить очередь", callback_data=QueueCallback(button="btn_6", id=id).pack(),style="danger")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def delete_kb(lenght, queue_id):
    kb_list = [[InlineKeyboardButton(text=str(i-1), callback_data=DeleteCallback(queue_id = queue_id, id=i-1).pack()),
                InlineKeyboardButton(text=str(i), callback_data=DeleteCallback(queue_id = queue_id, id=i).pack())]
                for i in range(2, lenght+1, 2)]
    if lenght%2 != 0: kb_list.append([InlineKeyboardButton(text=str(lenght), callback_data=DeleteCallback(queue_id = queue_id, id=lenght).pack())])
    kb_list.append([InlineKeyboardButton(text="Назад", callback_data=QueueCallback(button="back", id=queue_id).pack())])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
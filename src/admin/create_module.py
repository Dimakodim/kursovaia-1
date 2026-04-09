import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('module_name', type=str)
args = parser.parse_args()

path_to_modules = 'src/modules/'
os.mkdir(path_to_modules + args.module_name)

with open(path_to_modules + args.module_name + '/' + args.module_name + '_module.py', 'x') as f:
    f.write(
f"""import aiogram
from aiogram import Router
from .{args.module_name}_keyboard import *
from .{args.module_name}_db import *

{args.module_name}_router = Router()
"""
    )

with open(path_to_modules + args.module_name + '/' + args.module_name + '_keyboard.py', 'x') as f:
    f.write(
f"""from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def {args.module_name}_kb():
    kb_list = [[KeyboardButton(text="{args.module_name}")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
"""
    )

with open(path_to_modules + args.module_name + '/' + args.module_name + '_db.py', 'x') as f:
    pass
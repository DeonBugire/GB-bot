from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = types.KeyboardButton(text='Лису')
button2 = types.KeyboardButton(text='Собаку')
button3 = types.KeyboardButton(text='Панду')


keyboard1 = [
    [button1, button2, button3]
]


keyboard = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)


def make_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    keyboard = ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
    return keyboard
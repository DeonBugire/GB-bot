from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    keyboard = ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
    return keyboard

import random
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.fortune_keyboard import make_keyboard_fortune
import requests

# Роутер для гадания
fortune_router = Router()

available_authors = {
    'Шекспир': 'Shakespear.txt',
    'БГ': 'BG.txt',
    'Маршак': 'Marshak.txt'
}
available_lines = ['Еще одну', 'Хватит на сегодня']

class Choice(StatesGroup):
    author = State()
    line = State()
    another_line = State()

CHOICE_ANOTHER_LINE = 'Хватит или еще одну?'
FINISHED_MESSAGE = 'Надеюсь, вам понравилось. Удачного дня!'

@fortune_router.message(Command(commands=['Гадай']))
async def start(message: types.Message, state: FSMContext):
    await message.answer('По кому сегодня гадаем?', reply_markup=make_keyboard_fortune(available_authors.keys()))
    await state.set_state(Choice.author)

@fortune_router.message(Choice.author, F.text)
async def authors(message: types.Message, state: FSMContext):
    author = message.text
    if author in available_authors:
        filename = available_authors[author]
        with open(f'storage/{filename}', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_line = random.choice(lines).strip()
        await state.update_data(author=author, lines=lines, random_line=random_line)
        await message.answer(f'Вот вам строчка на сегодня: {random_line}')
        await message.answer(CHOICE_ANOTHER_LINE, reply_markup=make_keyboard_fortune(available_lines))
        await state.set_state(Choice.line)
    else:
        await message.answer('Такого в запасе, к сожалению, нет, выберите, пожалуйста, другого', reply_markup=make_keyboard_fortune(available_authors.keys()))

@fortune_router.message(Choice.line, F.text.in_(available_lines))
async def grade(message: types.Message, state: FSMContext):
    choice = message.text
    data = await state.get_data()
    if choice == 'Еще одну':
        random_line = random.choice(data['lines']).strip()
        await message.answer(f'Вот вам еще одна строчка: {random_line}')
        await state.update_data(random_line=random_line)
        await message.answer(CHOICE_ANOTHER_LINE, reply_markup=make_keyboard_fortune(available_lines))
    elif choice == 'Хватит на сегодня':
        await message.answer(FINISHED_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer('Ой, я так не умею, попробуйте еще раз, пожалуйста', reply_markup=make_keyboard_fortune(available_lines))

@fortune_router.message(Choice.line)
async def grade_incorrectly(message: types.Message):
    await message.answer('Ой, я так не умею, попробуйте еще раз, пожалуйста', reply_markup=make_keyboard_fortune(available_lines))
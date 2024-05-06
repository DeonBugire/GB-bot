import random
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.career_keyboard import make_keyboard

router = Router()

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

@router.message(Command(commands=['гадай']))
async def start(message: types.Message, state: FSMContext):
    await message.answer('По кому сегодня гадаем?', reply_markup=make_keyboard(available_authors.keys()))
    await state.set_state(Choice.author)

@router.message(Choice.author, F.text)
async def authors(message: types.Message, state: FSMContext):
    author = message.text
    if author in available_authors:
        filename = available_authors[author]
        with open(f'storage/{filename}', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            random_line = random.choice(lines).strip()
        await state.update_data(author=author, lines=lines, random_line=random_line)
        await message.answer(f'Вот вам строчка на сегодня: {random_line}')
        await message.answer(CHOICE_ANOTHER_LINE, reply_markup=make_keyboard(available_lines))
        await state.set_state(Choice.line)
    else:
        await message.answer('Такого в запасе, к сожалению, нет, выберите, пожалуйста, другого', reply_markup=make_keyboard(available_authors.keys()))

@router.message(Choice.line, F.text.in_(available_lines))
@router.message(Choice.another_line, F.text.in_(available_lines))
async def grade(message: types.Message, state: FSMContext):
    choice = message.text
    data = await state.get_data()
    random_line = random.choice(data['lines']).strip()
    if choice == 'Еще одну':
        await message.answer(f'Вот вам еще одна строчка: {random_line}')
        await state.update_data(random_line=random_line)
        await message.answer(CHOICE_ANOTHER_LINE, reply_markup=make_keyboard(available_lines))
        if choice == 'Еще одну':
            await state.set_state(Choice.another_line)
        else:
            await state.set_state(Choice.line)
    elif choice == 'Хватит на сегодня':
        await message.answer(FINISHED_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer('Ой, я так не умею, попробуйте еще раз, пожалуйста', reply_markup=make_keyboard(available_lines))

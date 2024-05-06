from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.animals_keyboard import make_keyboard
import requests

animals_router = Router()

available_animals = {
    'Лиса': 'https://randomfox.ca/floof/',
    'Собака': 'https://random.dog/woof.json',
    'Панда': 'https://some-random-api.ml/img/panda'
}
available_lines_animals = ['Конечно, еще одну!', 'Хватит на сегодня']

class ChoiceAnimals(StatesGroup):
    animal = State()
    line = State()
    another_line = State()

CHOICE_ANOTHER_LINE_ANIMALS = 'Хватит или еще одну?'
FINISHED_MESSAGE_ANIMALS = 'Надеюсь, вам понравилось. Удачного дня!'

@animals_router.message(Command(commands=['Милое']))
async def start_animals(message: types.Message, state: FSMContext):
    await message.answer('Какое животное хотите сегодня посмотреть?', reply_markup=make_keyboard(available_animals.keys()))
    await state.set_state(ChoiceAnimals.animal)

@animals_router.message(ChoiceAnimals.animal, F.text)
async def animals(message: types.Message, state: FSMContext):
    animal = message.text
    if animal in available_animals:
        url = available_animals[animal]
        response = requests.get(url)
        data = response.json()

        if animal == 'Лиса':
            image_url = data['image']
        elif animal == 'Собака':
            image_url = data['url']
        elif animal == 'Панда':
            image_url = data['link']

        await message.answer_photo(image_url)
        await message.answer(CHOICE_ANOTHER_LINE_ANIMALS, reply_markup=make_keyboard(available_lines_animals))
        await state.set_state(ChoiceAnimals.line)
    else:
        await message.answer('Такого животного нет в нашем списке.')

@animals_router.message(ChoiceAnimals.line, F.text.in_(available_lines_animals))
async def grade_animals(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == 'Конечно, еще одну!':
        await message.answer('Выберите животное:', reply_markup=make_keyboard(available_animals.keys()))
        await state.set_state(ChoiceAnimals.animal)
    elif choice == 'Хватит на сегодня':
        await message.answer(FINISHED_MESSAGE_ANIMALS, reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer('Выберите вариант из предложенных.')

@animals_router.message(ChoiceAnimals.line)
async def grade_incorrectly_animals(message: types.Message):
    await message.answer('Пожалуйста, выберите один из предложенных вариантов.')

@animals_router.message(ChoiceAnimals.another_line)
async def another_line_animals(message: types.Message):
    await message.answer('Пожалуйста, выберите один из предложенных вариантов.')
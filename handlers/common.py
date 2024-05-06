from aiogram import Router, types, F
from aiogram.filters.command import Command
from keyboards.keyboards import keyboard

router = Router()

@router.message(Command(commands=['start']))
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=keyboard)


@router.message(Command(commands=['стоп']))
@router.message(Command(commands=['stop']))
async def stop(message: types.Message):
    print(message.from_user.full_name)
    await message.answer(f'Прощай, {message.chat.first_name}, надеюсь, ты вернешься!')
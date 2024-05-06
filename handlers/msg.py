from aiogram import Router, types, F

router = Router()

@router.message(F.text)
async def msg(message: types.Message):
    if 'как дела' in message.text.lower():
        await message.reply('Нормально, а у тебя?')
    elif 'привет' in message.text.lower():
        await message.reply('И тебе привет!')
    elif 'пока' in message.text.lower():    
        await message.reply('Пока!')
    elif 'шутк' in message.text.lower():
        await message.reply('Прости, я сегодня не в настроении для шуток')
    else:
        await message.reply('Не понимаю тебя...')

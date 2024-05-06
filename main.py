import asyncio
import config
from aiogram import Bot, Dispatcher
import logging
from handlers import common, fortune_choice, msg, animal_choice


async def main():
    # Логирование
    logging.basicConfig(level=logging.INFO)

    # Объект бота и диспетчера
    bot = Bot(token=config.token)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(animal_choice.animals_router)
    dp.include_router(fortune_choice.fortune_router)
    dp.include_router(msg.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



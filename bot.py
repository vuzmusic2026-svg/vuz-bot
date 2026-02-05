import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# ТВОЙ САМЫЙ НОВЫЙ ТОКЕН
TOKEN = "8549618830:AAEgt90rAH8A0KE2q7A5GMDRgePWJu_UR5w"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Брат, VUŽ на связи! Теперь всё работает как надо. Погнали делать историю!")

async def main():
    print("БОТ ЗАПУЩЕН")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())















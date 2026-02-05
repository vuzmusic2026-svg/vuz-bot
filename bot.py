import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# НОВЫЙ ТОКЕН
TOKEN = "8549618830:AAG-_4yy9jlMrbTFjNi3z3RgfmmSZ_vWWUs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Брат, VUŽ в строю! 🐍\nТеперь всё чисто, работаем!")

async def main():
    print("🚀 БОТ ЗАПУЩЕН НА НОВОМ ТОКЕНЕ")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())











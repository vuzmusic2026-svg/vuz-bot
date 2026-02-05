import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = "8549618830:AAG-_4yy9jlMrbTFjNi3z3RgfmmSZ_vWWUs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Брат, VUŽ в строю! 🐍\nТеперь всё чётко. Давай делать «Дрыгву»!")

async def main():
    print("🚀 БОТ ЗАПУЩЕН")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())












import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# НОВЫЙ ТОКЕН
TOKEN = "8549618830:AAEl_d-iBGFMyIeg_QhQF-AoeHNZnqBXdNY"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Брат, VUŽ воскрес! 🐍\nТеперь всё идеально. Погнали делать историю!")

async def main():
    print("🚀 БОТ ЗАПУЩЕН НА НОВОМ ТОКЕНЕ")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())













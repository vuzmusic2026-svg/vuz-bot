import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import generativeai as genai

logging.basicConfig(level=logging.INFO)

# --- ДАННЫЕ ---
TOKEN = "8549618830:AAEQ9rkQZX_aT9L2MGz8tLBaYWjfI-27Bog"
GEMINI_API_KEY = "API_КЛЮЧ_GEMINI" # Если есть ключ, вставь сюда

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    buttons = [
        [types.KeyboardButton(text="📝 Сгенерировать пост")],
        [types.KeyboardButton(text="🎬 Сценарий для Reels")],
        [types.KeyboardButton(text="🎵 О проекте VUŽ")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Здорово, Брат! 🐍\nПроект VUŽ на связи.", reply_markup=get_main_keyboard())

@dp.message(lambda message: message.text == "🎵 О проекте VUŽ")
async def about_project(message: types.Message):
    await message.answer("Проект VUŽ — это Dark Folk-Rave. Качаем альбом «Лёс» и готовим «Дрыгву».")

@dp.message(lambda message: message.text == "📝 Сгенерировать пост")
async def generate_post(message: types.Message):
    await message.answer("Думаю над постом... ⏳")
    try:
        response = model.generate_content("Напиши короткий мрачный пост для TikTok про белорусское болото и мифологию.")
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    print("🚀 Шаг 2 активирован. Бот VUŽ в строю!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())










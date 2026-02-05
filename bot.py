import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ VUŽ ---
# Твой НОВЫЙ токен после revoke
TOKEN = "8549618830:AAEykK1AabSjxdFRXQeVy0PGlcvgl5W59jU"
# Твой ID канала
CHANNEL_ID = "-1002302324707"
# Ключ Gemini (Брат, проверь, чтобы он был вставлен полностью внутри кавычек)
GENAI_API_KEY = "AIzaSyD..."

# Настройка нейросети
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- КНОПКИ АДМИНКИ ---
def get_admin_kb():
    buttons = [
        [InlineKeyboardButton(text="📝 Сгенерировать пост", callback_data="gen_post")],
        [InlineKeyboardButton(text="📊 Создать опрос", callback_data="admin_poll")],
        [InlineKeyboardButton(text="🗑 Удалить это сообщение", callback_data="delete_msg")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_post_kb():
    buttons = [
        [InlineKeyboardButton(text="✅ Опубликовать", callback_data="confirm_post")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="delete_msg")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ОБРАБОТКА КОМАНД ---
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(f"Привет, Брат! Проект VUŽ на связи. Жми кнопку ниже для управления.", reply_markup=get_admin_kb())

# --- ГЕНЕРАЦИЯ ПОСТА ---
@dp.callback_query(F.data == "gen_post")
async def start_gen_post(callback: CallbackQuery):
    await callback.message.edit_text("🔮 Магия Gemini в процессе... Сочиняю пост про белорусские мифы.")
   
    prompt = "Напиши короткий, атмосферный пост для Telegram канала о белорусской мифологии в стиле Dark Folk. Используй мрачные эпитеты, лес, болото. В конце добавь хештег #VUŽ #Беларусь"
   
    try:
        response = model.generate_content(prompt)
        text = response.text
        await callback.message.edit_text(f"**Вариант поста:**\n\n{text}", reply_markup=get_post_kb())
    except Exception as e:
        await callback.message.edit_text(f"Ошибка нейросети: {e}", reply_markup=get_admin_kb())

# --- ПУБЛИКАЦИЯ ---
@dp.callback_query(F.data == "confirm_post")
async def confirm_post(callback: CallbackQuery):
    try:
        # Извлекаем текст поста
        msg_text = callback.message.text
        if "Вариант поста:" in msg_text:
            post_text = msg_text.split("Вариант поста:")[1].strip()
        else:
            post_text = msg_text
           
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
        await callback.answer("Готово! Пост улетел в канал.", show_alert=True)
        await callback.message.delete()
    except Exception as e:
        await callback.answer(f"Ошибка публикации: {e}", show_alert=True)

@dp.callback_query(F.data == "delete_msg")
async def delete_msg(callback: CallbackQuery):
    await callback.message.delete()

# --- ОПРОСЫ ---
@dp.callback_query(F.data == "admin_poll")
async def send_poll(callback: CallbackQuery):
    try:
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question="Какая энергия сегодня ближе?",
            options=["Ледяная тишина леса", "Ритм ночного рейва", "Шепот предков", "Зов болота"],
            is_anonymous=False
        )
        await callback.answer("Опрос запущен!")
    except Exception as e:
        await callback.answer(f"Ошибка: {e}")

# --- ЗАПУСК ---
async def main():
    # Очистка очереди обновлений
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Шаг 2 активирован. Бот VUŽ в строю!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())







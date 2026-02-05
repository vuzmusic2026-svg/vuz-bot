import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- НАСТРОЙКИ ---
TOKEN = "8549618830:AAGt4flgrDRSvnJVzmwp3qEYX53IMgaLXIk"
GOOGLE_API_KEY = "AIzaSyAXgQ9AaGjdc78LeFnnZQlKEJlgPZXPoOo"
ADMIN_ID = 7414696231
CHANNEL_ID = "@vuz_officeall"

# Настройка "мозгов" Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Личность твоего "Второго Я"
SYSTEM_PROMPT = (
    "Ты — цифровой двойник артиста VUŽ. Твой стиль: Dark Folk-Rave. "
    "Ты общаешься как 'брат', просто, честно, глубоко. "
    "Твои темы: белорусские болота, густые леса, старый деревенский быт, магия предков и тяжелый электронный звук. "
    "Пиши на русском языке. Тон: уверенный, немного мистический, мужской. "
    "Избегай лишних слов и смайликов. Иногда можно использовать 🐍. "
    "Твоя цель — писать посты для канала, которые заставляют задуматься о корнях."
)

# --- ГЛАВНОЕ МЕНЮ ---
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💿 Альбомы", callback_data="sub_albums"))
    builder.row(types.InlineKeyboardButton(text="📱 Соцсетки", callback_data="sub_socials"))
    if ADMIN_ID: # Кнопка только для тебя
        builder.row(types.InlineKeyboardButton(text="⚙️ Админка", callback_data="admin_panel"))
    return builder.as_markup()

def get_admin_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📝 Придумать пост", callback_data="ai_gen_post"))
    builder.row(types.InlineKeyboardButton(text="📊 Сделать опрос", callback_data="admin_poll"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    return builder.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Витаем у свеце VUŽ 🐍\nВыбирай свой путь:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "admin_panel")
async def admin_panel(callback: types.Callback_query):
    if callback.from_user.id == ADMIN_ID:
        await callback.message.edit_text("Здаров, брат. Что создадим?", reply_markup=get_admin_menu())

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.Callback_query):
    await callback.message.edit_text("Выбирай свой путь:", reply_markup=get_main_menu())

# --- ЛОГИКА ГЕНЕРАЦИИ ПОСТА ---
@dp.callback_query(F.data == "ai_gen_post")
async def ask_topic(callback: types.Callback_query):
    await callback.message.answer("Напиши мне тему поста. О чем сегодня расскажем братьям?")

@dp.message(F.from_user.id == ADMIN_ID)
async def handle_topic(message: types.Message):
    if message.text.startswith('/'): return # Игнорим команды
   
    status_msg = await message.answer("Связываюсь с духами леса (генерирую пост)...")
   
    try:
        # Запрос к нейронке
        prompt = f"{SYSTEM_PROMPT}\n\nНапиши короткий и мощный пост на тему: {message.text}"
        response = model.generate_content(prompt)
        ai_text = response.text

        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="✅ Опубликовать", callback_data="confirm_post"))
        builder.row(types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_msg"))
       
        await status_msg.delete()
        await message.answer(f"**Вариант поста:**\n\n{ai_text}", reply_markup=builder.as_markup(), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Брат, что-то с нейронкой: {e}")

@dp.callback_query(F.data == "confirm_post")
async def confirm_post(callback: types.Callback_query):
    # Берем текст из сообщения, убирая заголовок
    post_text = callback.message.text.split("**Вариант поста:**\n\n")[1]
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
        await callback.answer("Готово! Пост в канале.", show_alert=True)
        await callback.message.delete()
    except Exception as e:
        await callback.answer(f"Ошибка публикации: {e}", show_alert=True)

@dp.callback_query(F.data == "delete_msg")
async def delete_msg(callback: types.Callback_query):
    await callback.message.delete()

# --- ОПРОСЫ ---
@dp.callback_query(F.data == "admin_poll")
async def send_poll(callback: types.Callback_query):
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

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Шаг 2 активирован. Бот с 'мозгами' в строю!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

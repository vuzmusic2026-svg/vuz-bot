import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

# --- НАСТРОЙКИ ЛОГИРОВАНИЯ ---
logging.basicConfig(level=logging.INFO)

# --- КОНФИГ (ТВОИ КЛЮЧИ) ---
TOKEN = "8549618830:AAEgt90rAH8A0KE2q7A5GMDRgePWJu_UR5w"
GEMINI_KEY = "ТВОЙ_КЛЮЧ_GEMINI" # Брат, вставь сюда свой ключ Gemini API
CHANNEL_ID = "@vuz_officeall"
ADMIN_ID = 5650116892

# Настройка Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ТРЕКОВ (АЙДИ ИЗ ТВОЕГО СПИСКА) ---
VUZ_ALBUM = [
    "CQACAgIAAxkBAANaaYPDdB0ye-3T-PtLWzDEqAKqVGEAAoiOAALKiyBIDjV3diI8Epo4BA",
    "CQACAgIAAxkBAANcaYPDjXgSRxmU5Tv1DdBi9SccEO4AAomOAALKiyBI3yex3ocT3xM4BA",
    "CQACAgIAAxkBAANeaYPDk2xLJfyVY3kyhYXGhBni3IoAAoqOAALKiyBItDD_0kAS1D04BA",
    "CQACAgIAAxkBAANgaYPDmLiIFwWlzKJZvm7a8rkRDMwAAouOAALKiyBIdSKSYDQZx2c4BA",
    "CQACAgIAAxkBAANiaYPDn5Zd3ZQjoy1IEvwlxWPgdHQAAoyOAALKiyBIQpqq9XRnzPU4BA",
    "CQACAgIAAxkBAANkaYPDqKHkQ1ayVci7Z35N1d66cxkAAo2OAALKiyBIzWqf7k4DMVQ4BA",
    "CQACAgIAAxkBAANmaYPDsLFGDmdycbnD9zEx1pDj7CIAAo6OAALKiyBIJrhdst43hvY4BA",
    "CQACAgIAAxkBAANoaYPDtWyYF1Fsuq9jCuOBllsWse8AAo-OAALKiyBIDtT__FxoJxI4BA",
    "CQACAgIAAxkBAANqaYPDu9PY_DqTE3hLl6I1ZC0f-pwAApCOAALKiyBILGIphXz5G6E4BA",
    "CQACAgIAAxkBAANsaYPDwd3e6owRMb_OfQMitygYH3cAApGOAALKiyBIucOrfTLtF3M4BA",
    "CQACAgIAAxkBAANuaYPDyJAkhEkIcCGfcLYhZcUkxUEAApOOAALKiyBISLNr8PHagTI4BA",
    "CQACAgIAAxkBAANwaYPD0CZco62fv2JGI2dJAqQtomYAApSOAALKiyBIsfACLiDleVU4BA",
    "CQACAgIAAxkBAANyaYPD3fgGxpjjmrckzsqsY7WeLiQAApWOAALKiyBIs5aPYb3xV-44BA",
    "CQACAgIAAxkBAAN0aYPD4q9yK6NlpQ5xnU_8IdWbp4EAApaOAALKiyBIzM7mINaOzbU4BA",
    "CQACAgIAAxkBAAN2aYPD6P-JXmF2GoxUSgjLPaKkbWMAApeOAALKiyBICi4IPRaChxo4BA",
    "CQACAgIAAxkBAAN4aYPD75l5raQif3TRnvl4y1QF1ysAApiOAALKiyBIxjUd_tgRIUc4BA",
    "CQACAgIAAyEFAATFiccMAAOlaXz1Hq-bon6PKsTqr8Ywn_htN9oAAoSYAAJi6OhL-urgEwn-mpM4BA"
]

LYOS_ALBUM = [
    "CQACAgIAAxkBAAN_aYPIVyDTU9-4yRSclGIQU1piBpAAAoqEAAICLaBKrUJpdqBTjs84BA",
    "CQACAgIAAxkBAAOBaYPIZ7VO9ruRzxPKB0Ktad0SWf0AAiCIAAJRfFBKTX-Cekk75a84BA",
    "CQACAgIAAxkBAAODaYPIcWoBJR1hnb2nPgFd2hEG5-YAAuuJAAIET3FKOaYFLyB-ufw4BA",
    "CQACAgIAAxkBAAOFaYPIvgRjkvpnM5TxOfWedL8a_mwAAsSOAALKiyBIZYULgrYCUqw4BA",
    "CQACAgIAAxkBAAOHaYPIxBWfrUyMR5Ca4hUU3xD4GM4AAsqTAALvcphK0AABIKxakAp1OAQ",
    "CQACAgIAAxkBAAOJaYPIzpFuEjLpnGjO4RNl8qqTbooAAo-EAAICLaBKxAk8pOoUVj44BA",
    "CQACAgIAAxkBAAOLaYPJCu678iTkZkk9YvgIEZ0-ioAAAseOAALKiyBIFHKtT7eN6Fk4BA",
    "CQACAgIAAxkBAAONaYPJDFaJdPzhvAPpHFiWyMKt3r4AAmqWAAKicJlKBlBiYmILWsU4BA",
    "CQACAgIAAxkBAAOPaYPJP-g_5SUp1-Qf3t0QikbfqooAAqCAAAKgnthLmsIN1DXLSVI4BA",
    "CQACAgIAAxkBAAORaYPJ0dstYy33noleO5zHLmxkZBUAAsuOAALKiyBIv3X2-ZR3hxQ4BA",
    "CQACAgIAAxkBAAOTaYPKntTdt6cO34xf5wGvUCDko7EAAsyOAALKiyBIHLE2M-VdvU44BA"
]

# --- КЛАВИАТУРЫ ---
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💿 Альбомы", callback_data="albums"))
    builder.row(types.InlineKeyboardButton(text="📱 Соцсети", callback_data="socials"))
    builder.row(types.InlineKeyboardButton(text="🎬 Видео", callback_data="video"))
    builder.row(types.InlineKeyboardButton(text="🎧 Площадки", callback_data="platforms"))
    return builder.as_markup()

# --- ОБРАБОТКА ИИ (GEMINI) ---
async def get_ai_response(user_text):
    try:
        prompt = f"Ты — официальный ИИ-ассистент музыкального проекта VUŽ. Твой стиль: добрый, вдохновляющий, человечный. Ты помогаешь фанатам. Отвечай кратко, с любовью. Вопрос пользователя: {user_text}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Брат, я всегда рядом. Слушай музыку сердца. ❤️"

# --- ОБРАБОТЧИКИ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Вітаем у свеце VUŽ 🐍\nСлухай музыку без абмежаванняў.", reply_markup=main_menu())

@dp.callback_query(F.data == "albums")
async def albums(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐍 Я VUŽ", callback_data="vuz_album"))
    builder.row(types.InlineKeyboardButton(text="🌸 ЛЁС", callback_data="lyos_album"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main"))
    await callback.message.edit_text("Выбирай альбом:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.endswith("_album"))
async def show_tracks(callback: types.CallbackQuery):
    album_type = callback.data.split("_")[0]
    tracks = VUZ_ALBUM if album_type == "vuz" else LYOS_ALBUM
    builder = InlineKeyboardBuilder()
    for i, fid in enumerate(tracks, 1):
        builder.add(types.InlineKeyboardButton(text=f"🎵 Трек {i}", callback_data=f"play_{album_type}_{i-1}"))
    builder.adjust(3)
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="albums"))
    await callback.message.edit_text(f"Треки альбома {'Я VUŽ' if album_type == 'vuz' else 'ЛЁС'}:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("play_"))
async def play(callback: types.CallbackQuery):
    _, album, idx = callback.data.split("_")
    fid = VUZ_ALBUM[int(idx)] if album == "vuz" else LYOS_ALBUM[int(idx)]
    await callback.message.answer_audio(audio=fid, caption="VUŽ @vuz_officeall")

@dp.callback_query(F.data == "socials")
async def socials(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@vuz_music"))
    builder.row(types.InlineKeyboardButton(text="Telegram", url="https://t.me/vuz_officeall"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main"))
    await callback.message.edit_text("Нашы сацыяльныя сеткі:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "platforms")
async def platforms(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Яндекс Музыка", url="https://music.yandex.ru/artist/4500355"))
    builder.row(types.InlineKeyboardButton(text="VK Музыка", url="https://vk.com/artist/3174360383775460208"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main"))
    await callback.message.edit_text("Слухай нас на пляцоўках:", reply_markup=builder.as_markup())

# --- УМНОЕ ОБЩЕНИЕ (ИИ) И АДМИНКА ---
@dp.message(F.text)
async def handle_message(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="✅ В КАНАЛ", callback_data="post"))
        builder.row(types.InlineKeyboardButton(text="🤖 ОТВЕТ ИИ", callback_data="ai_answer"))
        await message.reply(f"Брат, что делаем с этим текстом?", reply_markup=builder.as_markup())
    else:
        # Обычный пользователь получает ответ от Gemini
        response = await get_ai_response(message.text)
        await message.answer(response)

@dp.callback_query(F.data == "post")
async def confirm_post(callback: types.CallbackQuery):
    text = callback.message.reply_to_message.text
    await bot.send_message(chat_id=CHANNEL_ID, text=f"✨ **VUŽ / НОВАЕ**\n\n{text}\n\n@vuz_officeall", parse_mode="Markdown")
    await callback.answer("Опубликовано!")
    await callback.message.delete()

@dp.callback_query(F.data == "main")
async def back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбирай раздел:", reply_markup=main_menu())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



















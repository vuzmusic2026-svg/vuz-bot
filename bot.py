import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

# --- ЛАГІРАВАННЕ ---
logging.basicConfig(level=logging.INFO)

# --- КАНФІГУРАЦЫЯ ---
TOKEN = "8549618830:AAEgt90rAH8A0KE2q7A5GMDRgePWJu_UR5w"
GEMINI_KEY = "УСТАЎ_СВОЙ_КЛЮЧ_GEMINI"
CHANNEL_ID = "@vuz_officeall"
ADMIN_ID = 5650116892

# Налада Gemini
genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ТРЭКАЎ ---

# Альбом «Лёс» (17 трэкаў)
LYOS_ALBUM = [
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

# Альбом «Я ВУЖ» (11 трэкаў)
VUZ_ALBUM = [
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

# --- КЛАВІЯТУРЫ ---
def get_main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💿 Альбомы", callback_data="albums"))
    builder.row(types.InlineKeyboardButton(text="📱 Сацыяльныя сеткі", callback_data="socials"))
    builder.row(types.InlineKeyboardButton(text="🎬 Відэа", callback_data="video"))
    builder.row(types.InlineKeyboardButton(text="🎧 Пляцоўкі", callback_data="platforms"))
    return builder.as_markup()

async def ask_gemini(text):
    try:
        prompt = f"Ты — афіцыйны ІІ-асістэнт музычнага праекта VUŽ. Ты размаўляеш на беларускай мове. Ты добры, шчыры і чалавечны. Адказвай каротка і з любоўю. Пытанне: {text}"
        res = ai_model.generate_content(prompt)
        return res.text
    except:
        return "Брат, музыка заўсёды ў сэрцы. ❤️"

# --- АПРАЦОЎШЧЫКІ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Вітаем у свеце VUŽ 🐍\nСлухай музыку без абмежаванняў.", reply_markup=get_main_kb())

@dp.callback_query(F.data == "albums")
async def albums_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🌸 Альбом «Лёс»", callback_data="list_lyos"))
    builder.row(types.InlineKeyboardButton(text="🐍 Альбом «Я ВУЖ»", callback_data="list_vuz"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    await callback.message.edit_text("Выбірай альбом:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("list_"))
async def list_tracks(callback: types.CallbackQuery):
    album = callback.data.split("_")[1]
    tracks = LYOS_ALBUM if album == "lyos" else VUZ_ALBUM
    builder = InlineKeyboardBuilder()
    for i, _ in enumerate(tracks, 1):
        builder.add(types.InlineKeyboardButton(text=f"🎵 Трэк {i}", callback_data=f"p_{album}_{i-1}"))
    builder.adjust(3)
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="albums"))
    album_name = "«Лёс»" if album == "lyos" else "«Я ВУЖ»"
    await callback.message.edit_text(f"Трэкі альбома {album_name}:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("p_"))
async def play_music(callback: types.CallbackQuery):
    _, album, idx = callback.data.split("_")
    fid = LYOS_ALBUM[int(idx)] if album == "lyos" else VUZ_ALBUM[int(idx)]
    await callback.message.answer_audio(audio=fid, caption="VUŽ — З любоўю. @vuz_officeall")

@dp.callback_query(F.data == "socials")
async def socials_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@vuz_music"))
    builder.row(types.InlineKeyboardButton(text="Telegram", url="https://t.me/vuz_officeall"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    await callback.message.edit_text("Нашы сацыяльныя сеткі:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "platforms")
async def platforms_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Яндэкс", url="https://music.yandex.ru/artist/4500355"))
    builder.row(types.InlineKeyboardButton(text="VK Музыка", url="https://vk.com/artist/3174360383775460208"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    await callback.message.edit_text("Слухай нас на пляцоўках:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "video")
async def video_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="YouTube", url="https://youtube.com/@vuz_official"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    await callback.message.edit_text("Нашы відэа:", reply_markup=builder.as_markup())

@dp.message(F.text)
async def handle_text(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="✅ У КАНАЛ", callback_data="post_now"))
        builder.row(types.InlineKeyboardButton(text="🤖 ІІ ПОСТ", callback_data="ai_post"))
        await message.reply("Брат, робім пост?", reply_markup=builder.as_markup())
    else:
        answer = await ask_gemini(message.text)
        await message.answer(answer)

@dp.callback_query(F.data == "post_now")
async def post_now(callback: types.CallbackQuery):
    text = callback.message.reply_to_message.text
    await bot.send_message(chat_id=CHANNEL_ID, text=f"✨ **НОВАЕ АД VUŽ**\n\n{text}\n\n🐍 @vuz_officeall", parse_mode="Markdown")
    await callback.answer("Апублікавана!")

@dp.callback_query(F.data == "ai_post")
async def ai_post(callback: types.CallbackQuery):
    text = callback.message.reply_to_message.text
    ai_text = await ask_gemini(f"Зрабі гэты тэкст для канала больш душэўным і прыгожым: {text}")
    await bot.send_message(chat_id=CHANNEL_ID, text=f"✨ **VUŽ / ДУМКІ**\n\n{ai_text}\n\n🐍 @vuz_officeall", parse_mode="Markdown")
    await callback.answer("ІІ пост гатовы!")

@dp.callback_query(F.data == "main_menu")
async def back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбірай раздзел:", reply_markup=get_main_kb())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




















import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# --- КОНФИГ ---
TOKEN = "8549618830:AAEgt90rAH8A0KE2q7A5GMDRgePWJu_UR5w"
CHANNEL_ID = "@vuz_officeall"
ADMIN_ID = 5650116892

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ТВОИ ТРЕКИ ---
# Первый список (Я VUŽ)
VUZ_TRACKS = [
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

# Второй список (ЛЁС)
LYOS_TRACKS = [
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

# --- МЕНЮ ---
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💿 Альбомы", callback_data="sub_albums"))
    builder.row(types.InlineKeyboardButton(text="📱 Соцсети", callback_data="sub_socials"))
    builder.row(types.InlineKeyboardButton(text="🎬 Видео", callback_data="sub_video"))
    builder.row(types.InlineKeyboardButton(text="🎧 Площадки", callback_data="sub_platforms"))
    return builder.as_markup()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("VUŽ 🐍\nВыбери раздел:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "sub_albums")
async def process_albums(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🐍 Альбом «Я VUŽ»", callback_data="menu_vuz"))
    builder.row(types.InlineKeyboardButton(text="🌸 Альбом «Лёс»", callback_data="menu_lyos"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    await callback.message.edit_text("Выбери альбом:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "menu_vuz")
async def vuz_list(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for i, fid in enumerate(VUZ_TRACKS, 1):
        builder.add(types.InlineKeyboardButton(text=f"Трек {i}", callback_data=f"vuz_{i-1}"))
    builder.adjust(3)
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="sub_albums"))
    await callback.message.edit_text("Альбом «Я VUŽ»:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "menu_lyos")
async def lyos_list(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for i, fid in enumerate(LYOS_TRACKS, 1):
        builder.add(types.InlineKeyboardButton(text=f"Трек {i}", callback_data=f"lyos_{i-1}"))
    builder.adjust(3)
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="sub_albums"))
    await callback.message.edit_text("Альбом «Лёс»:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith(("vuz_", "lyos_")))
async def play_track(callback: types.CallbackQuery):
    data = callback.data.split("_")
    idx = int(data[1])
    fid = VUZ_TRACKS[idx] if data[0] == "vuz" else LYOS_TRACKS[idx]
    await callback.message.answer_audio(audio=fid, caption="VUŽ @vuz_officeall")

@dp.callback_query(F.data == "sub_socials")
async def process_socials(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@vuz_music"))
    builder.row(types.InlineKeyboardButton(text="Telegram", url="https://t.me/vuz_officeall"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    await callback.message.edit_text("Соцсети:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "sub_platforms")
async def process_platforms(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Яндекс", url="https://music.yandex.ru/artist/4500355"))
    builder.row(types.InlineKeyboardButton(text="VK", url="https://vk.com/artist/3174360383775460208"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    await callback.message.edit_text("Площадки:", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "sub_video")
async def process_video(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="YouTube", url="https://youtube.com/@vuz_official"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
    await callback.message.edit_text("Видео:", reply_markup=builder.as_markup())

@dp.message(F.text, F.from_user.id == ADMIN_ID)
async def admin_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="✅ В канал", callback_data="post_it"))
    builder.row(types.InlineKeyboardButton(text="❌ Отмена", callback_data="back_to_main"))
    await message.reply(f"Брат, постим?\n\n{message.text}", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "post_it")
async def post_it(callback: types.CallbackQuery):
    text = callback.message.text.split("\n\n")[1]
    await bot.send_message(chat_id=CHANNEL_ID, text=text)
    await callback.answer("Готово")
    await callback.message.delete()

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("VUŽ 🐍\nВыбери раздел:", reply_markup=get_main_menu())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()


















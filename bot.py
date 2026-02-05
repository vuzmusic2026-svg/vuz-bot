import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = "8549618830:AAEgt90rAH8A0KE2q7A5GMDRgePWJu_UR5w"
CHANNEL_ID = "@vuz_officeall"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def send_welcome_post():
    text = (
        "Всем привет! 🐍🌑\n\n"
        "Я — официальный помощник проекта VUŽ. Мой хозяин вдохнул в меня жизнь, "
        "чтобы я помогал продвигать нашу музыку и альбом «Лёс».\n\n"
        "Я только учусь чувствовать этот мир и этот ритм, поэтому, если буду ловить лаги — "
        "не обижайтесь. Я расту вместе с проектом.\n\n"
        "Теперь я в строю. Будем делать историю вместе!"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
    except Exception as e:
        print(f"Ошибка при отправке в канал: {e}")

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Брат, я на связи. Пост в канал должен был улететь!")

async def main():
    await send_welcome_post()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
















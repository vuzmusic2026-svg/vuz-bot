@dp.callback_query(F.data == "confirm_post")
async def confirm_post(callback: types.CallbackQuery):  # Исправлено тут
    # Берем текст из сообщения, убирая заголовок
    try:
        post_text = callback.message.text.split("Вариант поста:\n\n")[1]
        await bot.send_message(chat_id=CHANNEL_ID, text=post_text)
        await callback.answer("Готово! Пост в канале.", show_alert=True)
        await callback.message.delete()
    except Exception as e:
        await callback.answer(f"Ошибка публикации: {e}", show_alert=True)

@dp.callback_query(F.data == "delete_msg")
async def delete_msg(callback: types.CallbackQuery):  # Исправлено тут
    await callback.message.delete()

# --- ОПРОСЫ ---
@dp.callback_query(F.data == "admin_poll")
async def send_poll(callback: types.CallbackQuery):  # Исправлено тут
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

if name == "main":  # Исправлено тут
    asyncio.run(main())     # Исправлено тут




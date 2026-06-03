import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = -1002995313257

dp = Dispatcher()


# 🌐 веб-сервер для Render (антисон через HTTP)
async def handle(request):
    return web.Response(text="ok")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()


# 📩 обработка сообщений
@dp.channel_post()
async def handler(message: Message, bot: Bot):

    if message.chat.id != CHANNEL_ID:
        return

    if not message.text:
        return

    text = message.text.strip()

    # реагирует только на "пчол"
    if not text.lower().startswith("пчол"):
        return

    text = text[4:].strip()

    if not text:
        return

    # просто отвечает текстом без добавок
    await bot.send_message(CHANNEL_ID, text)


# 🚀 запуск
async def main():
    bot = Bot(TOKEN)

    asyncio.create_task(start_web())

    await dp.start_polling(bot)


asyncio.run(main())

import os
import random
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from aiohttp import web

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

answers = [
    "🐝 да",
    "🐝 нет",
    "🐝 скорее да",
    "🐝 скорее нет",
    "🐝 определённо да",
    "🐝 определённо нет",
    "🐝 пчолки считают что да",
    "🐝 пчолки считают что нет",
    "🐝 королева улья подтвердила",
    "🐝 все пчолы проголосовали за",
    "🐝 все пчолы проголосовали против",
    "🐝 шанс высокий",
    "🐝 шанс низкий",
    "🐝 вселенная занята",
    "🐝 ответ в сотах"
]

# ===== КАНАЛ =====
@dp.channel_post(F.text.lower().startswith("пчол "))
async def bee_handler(message: Message):
    question = message.text[5:].strip()
    if not question:
        return

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"❓ {question}\n\n{random.choice(answers)}"
    )

# ===== ПИНГ СЕРВЕР =====
async def handle(request):
    return web.Response(text="bot alive 🐝")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()

# ===== СТАРТ =====
async def main():
    await start_web()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

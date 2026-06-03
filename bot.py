import asyncio
import os
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

CHANNEL_ID = -1002995313257

dp = Dispatcher()

memory = [
    {
        "role": "system",
        "content": "ты помощник пчолкиGPT. отвечай кратко и по делу на русском."
    }
]


# 🌐 чтобы Render не засыпал
async def handle(request):
    return web.Response(text="ok")

async def start_web():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()


# 🤖 ИИ запрос
async def ask_ai(text: str):
    memory.append({"role": "user", "content": text})

    if len(memory) > 20:
        memory.pop(1)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": memory
            }
        ) as resp:

            data = await resp.json()

            if "choices" not in data:
                return "ошибка"

            answer = data["choices"][0]["message"]["content"]

            memory.append({"role": "assistant", "content": answer})

            return answer


# 📩 реагирует только на "пчол"
@dp.channel_post()
async def handler(message: Message, bot: Bot):

    if message.chat.id != CHANNEL_ID:
        return

    if not message.text:
        return

    text = message.text.strip()

    if not text.lower().startswith("пчол"):
        return

    text = text[4:].strip()

    if not text:
        return

    answer = await ask_ai(text)

    await bot.send_message(CHANNEL_ID, answer)


# 🚀 запуск
async def main():
    bot = Bot(TOKEN)

    asyncio.create_task(start_web())

    await dp.start_polling(bot)


asyncio.run(main())

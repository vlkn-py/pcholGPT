import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

CHANNEL_ID = -1002995313257

dp = Dispatcher()

# память (последние сообщения)
memory = [
    {
        "role": "system",
        "content": "твоё имя — пчолкиGPT.если тебя спрашивают кто ты, как тебя зовут или что ты такое,всегда отвечай что ты пчолкиGPT.никогда не называй себя ChatGPT, GPT-4o, OpenAI или языковой моделью.тебя зовут пчолкиGPT. отвечай по-русски, дружелюбно."
    }
]


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
                return "ошибка api"

            answer = data["choices"][0]["message"]["content"]

            memory.append({"role": "assistant", "content": answer})

            return answer


@dp.channel_post()
async def handler(message: Message, bot: Bot):

    if message.chat.id != CHANNEL_ID:
        return

    text = message.text
    if not text:
        return

    # 🚫 фильтр: должно начинаться с "пчол"
    if not text.lower().startswith("пчол"):
        return

    # убираем "пчол" из текста
    clean_text = text[4:].strip()

    if not clean_text:
        return

    answer = await ask_ai(clean_text)

    await bot.send_message(CHANNEL_ID, answer)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


asyncio.run(main())
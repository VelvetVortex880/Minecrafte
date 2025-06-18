"""GPT-controlled command sender for the Minecraft bot.

This script accepts instructions from the user, sends them to the OpenAI
API with a prompt to translate the instruction into Mineflayer JavaScript,
then forwards the resulting code to the bot via WebSocket.
"""

import asyncio
import os

import openai
import websockets
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You're controlling a Minecraft bot. "
    "Translate user instructions into JavaScript commands using the Mineflayer API. "
    "Respond with only the JavaScript code to execute."
)

BOT_URI = os.getenv("BOT_URI", "ws://localhost:3001")

async def send_instruction(instruction: str) -> None:
    """Send a single instruction to GPT-4 and forward the JS code to the bot."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": instruction},
        ],
    )

    code = response["choices"][0]["message"]["content"].strip()
    print("Generated JavaScript:\n" + code)

    async with websockets.connect(BOT_URI) as ws:
        await ws.send(code)
        reply = await ws.recv()
        print("Bot replied:", reply)

async def main() -> None:
    print("Connected to GPT server. Type instructions for the Minecraft bot.")
    while True:
        try:
            user_text = input("bot> ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_text.lower() in {"quit", "exit"}:
            break
        await send_instruction(user_text)

if __name__ == "__main__":
    asyncio.run(main())

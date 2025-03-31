import os
import gettext
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
# from openai import OpenAI
from dotenv import load_dotenv

from database import Database
from chat import MyChatGPT

load_dotenv()

# openAI_client = OpenAI(
#   api_key=os.getenv("OPENAI_KEY")
# )

TOKEN = os.getenv("BOT_TOKEN")
# DB_DSN = os.getenv("DB_DSN")    #"postgresql://user:password@localhost/mydatabase"

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
DB_DSN = f"postgresql://{USER}:{PASSWORD}@localhost/{DB}"

bot = Bot(token=TOKEN)
dp = Dispatcher()
database = Database(DB_DSN)
chatgpt = MyChatGPT(database)


def get_translator(lang):
    return gettext.translation("bot", localedir="locales", languages=[lang], fallback=True)

async def keep_typing(chat_id):
    asyncio.sleep(5)    # wait before "typing" the text
    while True:
        await bot.send_chat_action(chat_id, "typing")
        await asyncio.sleep(4)  # Refresh every 4s (before 5s limit)


# /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    user = message.from_user

    lang = message.from_user.language_code  # Get user’s language
    # lang = "ru"
    _ = get_translator(lang).gettext  # Load correct translation

    ans = await database.add_user(user.id)  # adds user id to db

    if ans == -1:
        response = _("You already have an active chat!\nSend a message to continue your convesation with your tutor.")

    else:
        response = _(
            "Hello, {first_name}!\nYour ID: {id}\nUsername: @{username}"
        ).format(
            first_name=user.first_name,
            id=user.id,
            username=f"{user.username}" if user.username else _("no username")
        )

    await message.answer(response)

@dp.message()
async def message_handler(message: Message):
    user_info = f"Received message from {message.from_user.full_name} (ID: {message.from_user.id})"
    print(user_info)  # Log user info (use dp.message.middleware(LoggingMiddleware()); class LoggingMiddleware(BaseMiddleware):)
    print("\tQ:", message.text)

    task = asyncio.create_task(keep_typing(message.chat.id)) # change this (message.chat.id) if you ever plan on adding groupchat support
    answer = await chatgpt.message_chatgpt(message.text, message.from_user.id)
    task.cancel()

    print("\tA:", answer)
    await message.answer(answer)


async def main():
    print("Bot is running!")
    await database.connect()
    await dp.start_polling(bot)
    await database.close()

if __name__ == "__main__":
    asyncio.run(main())
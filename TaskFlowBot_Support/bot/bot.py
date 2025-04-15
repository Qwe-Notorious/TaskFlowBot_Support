import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import config

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Open Mini App", web_app=types.WebAppInfo(
            url="https://taskflowbot-bo3ebae89oc55y7uotmcae.streamlit.app/"))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Hello!", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

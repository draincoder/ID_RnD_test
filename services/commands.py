from aiogram import types
from aiogram.dispatcher import Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("library", "Моя библиотека")
    ])

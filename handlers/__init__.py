from aiogram import Dispatcher

from .user import register_user
from .history import register_history


def register_handlers(dp: Dispatcher):
    register_history(dp)
    register_user(dp)

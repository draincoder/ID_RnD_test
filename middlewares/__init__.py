from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .role import RoleMiddleware
from .db import DbMiddleware


def setup_middlewares(dp: Dispatcher, **kwargs):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(RoleMiddleware(kwargs['admin_ids']))
    dp.middleware.setup(DbMiddleware(kwargs['async_session']))

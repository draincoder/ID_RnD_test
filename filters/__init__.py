from aiogram import Dispatcher
from .role import AdminFilter, RoleFilter
from .chat import PrivateChat, PublicChat


def register_filters(dp: Dispatcher):
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(PrivateChat)
    dp.filters_factory.bind(PublicChat)

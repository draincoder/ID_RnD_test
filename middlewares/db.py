from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import Database


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session: AsyncSession = session

    async def pre_process(self, obj, data, *args):
        session = self.session
        data["session"] = session
        data["db"] = Database(session)

    async def post_process(self, obj, data, *args):
        del data["db"]

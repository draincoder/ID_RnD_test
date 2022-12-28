import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import load_config
from database.base import Base
from filters import register_filters
from handlers import register_handlers
from middlewares import setup_middlewares
from services.commands import set_default_commands

logger = logging.getLogger(__name__)


async def main():
    fmt_str = "[%(asctime)s] - %(levelname)s - [%(module)s:%(lineno)s:%(funcName)s] - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt_str)

    logger.info("Starting bot")
    config = load_config("bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}',
        future=True)

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    setup_middlewares(dp, async_session=async_session, admin_ids=config.tg_bot.admin_ids)
    register_filters(dp)
    register_handlers(dp)

    try:
        await set_default_commands(dp)
        if config.tg_bot.skip_updates:
            await dp.skip_updates()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        async with async_session() as session:
            await session.close()


def start():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped!")


if __name__ == '__main__':
    start()

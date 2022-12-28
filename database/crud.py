import datetime
import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import File

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, db_session: AsyncSession):
        self.session: AsyncSession = db_session

    async def add_file(self, user_id: int, file_type: str, file_format: str, file_id: str, filename: str):
        async with self.session() as session:
            session.add(File(user_id=user_id, file_type=file_type, file_format=file_format,
                             file_id=file_id, filename=filename,
                             time=datetime.datetime.now().strftime('%H:%M %d.%m.%Y')))
            await session.commit()

    async def get_files(self, user_id: int) -> List[File]:
        async with self.session() as session:
            audios = await session.execute(select(File).where(File.user_id == user_id))
            return audios.scalars().all()

    async def get_file(self, id: int) -> File:
        async with self.session() as session:
            file = await session.get(File, id)
            return file

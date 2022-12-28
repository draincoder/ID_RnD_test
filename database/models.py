from sqlalchemy import Column, BigInteger, TEXT
from .base import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    file_id = Column(TEXT)
    filename = Column(TEXT)
    file_type = Column(TEXT)
    file_format = Column(TEXT)
    time = Column(TEXT)

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.database.pg.config import DBConfig

config = DBConfig()
engine = create_async_engine(config.url)
session_maker = async_sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    ...

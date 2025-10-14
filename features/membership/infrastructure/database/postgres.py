import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import NullPool


logger = logging.getLogger(__name__)


class DbConnection:
    def __init__(self, db_url: str):
        if not db_url:
            raise Exception("Database URL is required")

        self.engine = create_async_engine(db_url, poolclass=NullPool)

        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
            raise e
        finally:
            await session.close()

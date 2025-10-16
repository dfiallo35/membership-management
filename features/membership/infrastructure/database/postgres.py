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
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.exception("Database transaction failed: %s", e)
                raise

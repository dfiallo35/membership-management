import pytest_asyncio
from httpx import ASGITransport
from httpx import AsyncClient
from factory.alchemy import SQLAlchemyModelFactory

from features.membership.infrastructure.entities.base_model import BaseModel
from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.infrastructure.entities.gym_model import GymModel
from features.membership.infrastructure.entities.membership_model import MembershipModel

from main import app
from main import container


@pytest_asyncio.fixture(scope="function")
async def db_connection():
    db = container.db_connection()
    yield db
    await db.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_db(db_connection: DbConnection):
    async with db_connection.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


class AsyncBaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def create_async(cls, **kwargs):
        if cls._meta.sqlalchemy_session is None:
            raise ValueError(
                "sqlalchemy_session must be set before calling create_async()"
            )

        obj = cls(**kwargs)
        await cls._meta.sqlalchemy_session.commit()
        await cls._meta.sqlalchemy_session.refresh(obj)
        return obj


class GymFactory(AsyncBaseFactory):
    class Meta:
        model = GymModel


class MembershipFactory(AsyncBaseFactory):
    class Meta:
        model = MembershipModel


@pytest_asyncio.fixture
async def create_gym(db_connection):
    async with db_connection.get_session() as session:
        GymFactory._meta.sqlalchemy_session = session
        gym = await GymFactory.create_async(
            id="5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
            name="Test",
        )
        yield gym


@pytest_asyncio.fixture
async def create_membership_daily(db_connection):
    async with db_connection.get_session() as session:
        MembershipFactory._meta.sqlalchemy_session = session
        membership = await MembershipFactory.create_async(
            id="bbb05088-02ca-473f-972a-ca2ec1792e7f",
            name="Test",
            description="Test",
            duration_days=1,
            price=1,
            is_active=True,
            gym_id="5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
        )
        yield membership


@pytest_asyncio.fixture
async def create_membership_by_name(db_connection):
    async with db_connection.get_session() as session:
        MembershipFactory._meta.sqlalchemy_session = session
        membership = await MembershipFactory.create_async(
            id="0c22e23d-0d74-45a9-b94a-b0052cb11965",
            name="Test 2",
            description="Test",
            duration_days=10,
            price=1,
            is_active=False,
            gym_id="5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
        )
        yield membership

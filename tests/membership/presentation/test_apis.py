import pytest
import pytest_asyncio
from uuid import uuid4
from httpx import AsyncClient
from httpx import ASGITransport
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


class TestMembershipList:
    url = "/memberships/"

    @pytest.mark.asyncio
    async def test_list_memberships(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        response = await async_client.get(self.url)
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestMembershipGet:
    url = "/memberships/{id_membership}"

    @pytest.mark.asyncio
    async def test_get_membership_fail(self, async_client: AsyncClient, create_gym):
        id = uuid4()
        response = await async_client.get(self.url.format(id_membership=id))
        assert response.status_code == 404
        assert response.json()["message"] == f"Membership with id '{id}' not found"

    @pytest.mark.asyncio
    async def test_get_membership_success(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        response = await async_client.get(
            self.url.format(id_membership=create_membership_daily.id)
        )
        assert response.status_code == 200


class TestMembershipCreate:
    url = "/memberships/"

    @pytest.mark.asyncio
    async def test_create_membership_success(
        self, async_client: AsyncClient, create_gym
    ):
        response = await async_client.post(
            self.url,
            json={
                "name": "Test",
                "description": "Test",
                "duration_days": 1,
                "price": 1,
                "is_active": True,
                "gym_id": "5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
            },
        )
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_membership_fail_daily(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        response = await async_client.post(
            self.url,
            json={
                "name": "Test 2",
                "description": "Test 2",
                "duration_days": 1,
                "price": 1,
                "is_active": True,
                "gym_id": "5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
            },
        )
        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "Daily membership already exists for gym '5fc29d36-21b8-44dc-9c0d-a54ab5391b21'"
        )

    @pytest.mark.asyncio
    async def test_create_membership_fail_name(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        response = await async_client.post(
            self.url,
            json={
                "name": "Test",
                "description": "Test",
                "duration_days": 10,
                "price": 1,
                "is_active": True,
                "gym_id": "5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
            },
        )
        assert response.status_code == 400
        assert (
            response.json()["message"] == "Membership with name 'Test' already exists"
        )

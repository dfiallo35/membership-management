from uuid import UUID
import pytest
import pytest_asyncio
from uuid import uuid4
from httpx import AsyncClient
from httpx import ASGITransport

from features.membership.infrastructure.entities.base_model import BaseModel
from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.infrastructure.entities.gym_model import GymModel

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


@pytest_asyncio.fixture
async def create_gym(db_connection: DbConnection):
    async with db_connection.get_session() as session:
        gym = GymModel(
            id=UUID("5fc29d36-21b8-44dc-9c0d-a54ab5391b21"),
            name="Test",
        )
        session.add(gym)
        await session.commit()
    yield gym


class TestMembershipList:
    url = "/memberships/"

    @pytest.mark.asyncio
    async def test_list_memberships(self, async_client: AsyncClient, create_gym):
        response = await async_client.get(self.url)
        assert response.status_code == 200


class TestMembershipGet:
    url = "/memberships/{id_membership}"

    @pytest.mark.asyncio
    async def test_get_membership_fail(self, async_client: AsyncClient, create_gym):
        id = uuid4()
        response = await async_client.get(self.url.format(id_membership=id))
        assert response.status_code == 404
        assert response.json()["message"] == f"Membership with id '{id}' not found"

    # @pytest.mark.asyncio
    # async def test_get_membership_success(self, client: AsyncClient):
    #     response = await client.get(self.url.format(id_membership="5fc29d36-21b8-44dc-9c0d-a54ab5391b21"))
    #     assert response.status_code == 200


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
        self, async_client: AsyncClient, create_gym
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

    # @pytest.mark.asyncio
    # async def test_create_membership_fail_name(self, client: AsyncClient):
    #     response = await client.post(self.url, json={
    #         "name": "Test",
    #         "description": "Test",
    #         "duration_days": 10,
    #         "price": 1,
    #         "is_active": True,
    #         "gym_id": "5fc29d36-21b8-44dc-9c0d-a54ab5391b21",
    #     })
    #     assert response.status_code == 400
    #     assert response.json()["message"] == "Membership with name 'Test' already exists"

import pytest

from uuid import uuid4
from httpx import AsyncClient


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


class TestMembershipUpdate:
    url = "/memberships/{id_membership}"

    @pytest.mark.asyncio
    async def test_update_membership_fail_not_found(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        id = uuid4()
        response = await async_client.put(
            self.url.format(id_membership=id),
            json={"name": "New name"},
        )
        assert response.status_code == 404
        assert response.json()["message"] == f"Membership with id '{id}' not found"

    @pytest.mark.asyncio
    async def test_update_membership_fail_already_exists(
        self,
        async_client: AsyncClient,
        create_gym,
        create_membership_daily,
        create_membership_by_name,
    ):
        id = create_membership_by_name.id
        response = await async_client.put(
            self.url.format(id_membership=id),
            json={"name": "Test"},
        )
        assert response.status_code == 400
        assert (
            response.json()["message"] == "Membership with name 'Test' already exists"
        )

    @pytest.mark.asyncio
    async def test_update_membership_fail_daily(
        self,
        async_client: AsyncClient,
        create_gym,
        create_membership_daily,
        create_membership_by_name,
    ):
        id = create_membership_by_name.id
        response = await async_client.put(
            self.url.format(id_membership=id),
            json={"duration_days": 1},
        )
        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "Daily membership already exists for gym '5fc29d36-21b8-44dc-9c0d-a54ab5391b21'"
        )

    @pytest.mark.asyncio
    async def test_update_membership_success(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        id = create_membership_daily.id
        response = await async_client.put(
            self.url.format(id_membership=id),
            json={"name": "New name"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New name"


class TestMembershipDelete:
    url = "/memberships/{id_membership}"

    @pytest.mark.asyncio
    async def test_delete_membership_fail_not_found(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        id = uuid4()
        response = await async_client.delete(
            self.url.format(id_membership=id),
        )
        assert response.status_code == 404
        assert response.json()["message"] == f"Membership with id '{id}' not found"

    @pytest.mark.asyncio
    async def test_delete_membership_fail_in_use(
        self, async_client: AsyncClient, create_gym, create_membership_daily
    ):
        id = create_membership_daily.id
        response = await async_client.delete(
            self.url.format(id_membership=id),
        )
        assert response.status_code == 400
        assert (
            response.json()["message"]
            == "Membership with id 'bbb05088-02ca-473f-972a-ca2ec1792e7f' is in use"
        )

    @pytest.mark.asyncio
    async def test_delete_membership_success(
        self, async_client: AsyncClient, create_gym, create_membership_by_name
    ):
        id = create_membership_by_name.id
        response = await async_client.delete(
            self.url.format(id_membership=id),
        )
        assert response.status_code == 204

from fastapi import APIRouter
from fastapi import status

from features.membership.application.dtos.membership_dtos import (
    MembershipCreateRequest,
    MembershipPublic,
    MembershipUpdateRequest,
)
from features.membership.presentation.controllers.membership_controller import (
    MembershipController,
)


router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def create_membership(membership: MembershipCreateRequest):
    controller = MembershipController()
    return await controller.create_membership(membership)


@router.get(
    "/daily",
    response_model=MembershipPublic,
    status_code=status.HTTP_200_OK,
)
async def get_daily_membership():
    controller = MembershipController()
    return await controller.get_daily_membership()


@router.get(
    "/{id_membership}",
    response_model=MembershipPublic,
    status_code=status.HTTP_200_OK,
)
async def get_membership_by_id(id_membership: str):
    controller = MembershipController()
    return await controller.get_membership_by_id(id_membership)


@router.get(
    "/",
    response_model=list[MembershipPublic],
    status_code=status.HTTP_200_OK,
)
async def get_memberships():
    controller = MembershipController()
    return await controller.get_memberships()


@router.put(
    "/{id_membership}",
    response_model=MembershipPublic,
    status_code=status.HTTP_200_OK,
)
async def update_membership(
    membership_update: MembershipUpdateRequest, id_membership: str
):
    controller = MembershipController()
    return await controller.update_membership(id_membership, membership_update)


@router.delete(
    "/{id_membership}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_membership(id_membership: str):
    controller = MembershipController()
    return await controller.delete_membership(id_membership)

from fastapi import APIRouter
from fastapi import status

from features.membership.application.dtos.membership_dtos import (
    MembershipCreateRequest,
    MembershipPublic,
    MembershipUpdateRequest,
)
from features.membership.application.errors.membership_errors import ErrorResponse
from features.membership.presentation.controllers.membership_controller import (
    MembershipController,
)


router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": MembershipPublic},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_membership(membership: MembershipCreateRequest):
    controller = MembershipController()
    return await controller.create_membership(membership)


@router.get(
    "/daily",
    responses={
        status.HTTP_200_OK: {"model": MembershipPublic},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_daily_membership():
    controller = MembershipController()
    return await controller.get_daily_membership()


@router.get(
    "/{id_membership}",
    responses={
        status.HTTP_200_OK: {"model": MembershipPublic},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_membership_by_id(id_membership: str):
    controller = MembershipController()
    return await controller.get_membership_by_id(id_membership)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": list[MembershipPublic]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def get_memberships():
    controller = MembershipController()
    return await controller.get_memberships()


@router.put(
    "/{id_membership}",
    responses={
        status.HTTP_200_OK: {"model": MembershipPublic},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
)
async def update_membership(
    membership_update: MembershipUpdateRequest, id_membership: str
):
    controller = MembershipController()
    return await controller.update_membership(id_membership, membership_update)


@router.delete(
    "/{id_membership}",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_membership(id_membership: str):
    controller = MembershipController()
    return await controller.delete_membership(id_membership)

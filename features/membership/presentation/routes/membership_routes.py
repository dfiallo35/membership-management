from fastapi import APIRouter
from fastapi import status

from features.membership.application.dtos.membership_dtos import MembershipResponse
from features.membership.presentation.controllers.membership_controller import (
    MembershipController,
)


router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def create_membership():
    controller = MembershipController()
    return await controller.create_membership()


@router.get("/daily")
async def get_daily_membership(): ...


@router.get(
    "/{id_membership}",
    response_model=MembershipResponse,
    status_code=status.HTTP_200_OK,
)
async def get_membership_by_id(id_membership: str):
    controller = MembershipController()
    return await controller.get_membership_by_id(id_membership)


@router.get(
    "/",
    response_model=list[MembershipResponse],
    status_code=status.HTTP_200_OK,
)
async def get_memberships():
    controller = MembershipController()
    return await controller.get_memberships()


@router.put("/{id_membership}")
async def update_membership(): ...


@router.delete("/{id_membership}")
async def delete_membership(): ...

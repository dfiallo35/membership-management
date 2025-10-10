from fastapi import APIRouter

from features.membership.presentation.controllers.membership_controller import (
    MembershipController,
)


router = APIRouter(prefix="/memberships", tags=["Memberships"])


@router.post("/")
async def create_membership():
    controller = MembershipController()
    return await controller.create_membership()


@router.get("/daily")
async def get_daily_membership(): ...


@router.get("/{id_membership}")
async def get_membership_by_id(id_membership: str): ...


@router.get("/")
async def get_memberships(): ...


@router.put("/{id_membership}")
async def update_membership(): ...


@router.delete("/{id_membership}")
async def delete_membership(): ...

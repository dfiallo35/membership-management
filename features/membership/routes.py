from fastapi import APIRouter

from features.membership.presentation.routes.membership_routes import (
    router as membership_router,
)

router = APIRouter()

router.include_router(membership_router)

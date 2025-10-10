from features.membership.application.service import MembershipService
from features.membership.application.dtos.membership_dtos import (
    MembershipCreateRequest,
    MembershipResponse,
)


class MembershipController:
    def __init__(self):
        self.service = MembershipService()

    async def create_membership(
        self, membership: MembershipCreateRequest
    ) -> MembershipResponse:
        return await self.service.create_membership(membership)

    async def get_daily_membership(self): ...

    async def get_membership_by_id(self, membership_id: str) -> MembershipResponse:
        return await self.service.get_membership_by_id(membership_id)

    async def get_memberships(self) -> list[MembershipResponse]:
        return await self.service.list_memberships()

    async def update_membership(self): ...

    async def delete_membership(self): ...

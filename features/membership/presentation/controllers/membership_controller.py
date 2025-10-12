from features.membership.application.service import MembershipService
from features.membership.application.dtos.membership_dtos import (
    MembershipCreateRequest,
    MembershipPublic,
    MembershipUpdateRequest,
)


class MembershipController:
    def __init__(self):
        self.service = MembershipService()

    async def create_membership(
        self, membership: MembershipCreateRequest
    ) -> MembershipPublic:
        return await self.service.create_membership(membership)

    async def get_daily_membership(self) -> MembershipPublic | None:
        return await self.service.get_daily_membership()

    async def get_membership_by_id(self, membership_id: str) -> MembershipPublic:
        return await self.service.get_membership_by_id(membership_id)

    async def get_memberships(self) -> list[MembershipPublic]:
        return await self.service.list_memberships()

    async def update_membership(
        self, membership_id: str, membership_update: MembershipUpdateRequest
    ) -> MembershipPublic:
        return await self.service.update_membership(membership_id, membership_update)

    async def delete_membership(self, membership_id: str) -> None:
        return await self.service.delete_membership(membership_id)

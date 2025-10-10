from features.membership.application.service import MembershipService
from features.membership.application.dtos.membership_dtos import MembershipResponse


class MembershipController:
    def __init__(self):
        self.service = MembershipService()

    async def create_membership(self):
        return await self.service.create_membership()

    async def get_daily_membership(self): ...

    async def get_membership_by_id(self): ...

    async def get_memberships(self) -> list[MembershipResponse]:
        return await self.service.list_memberships()

    async def update_membership(self): ...

    async def delete_membership(self): ...

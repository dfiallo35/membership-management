from features.membership.application.service import MembershipService


class MembershipController:
    def __init__(self):
        self.service = MembershipService()

    async def create_membership(self):
        return await self.service.create_membership()

    async def get_daily_membership(self): ...

    async def get_membership_by_id(self): ...

    async def get_memberships(self): ...

    async def update_membership(self): ...

    async def delete_membership(self): ...

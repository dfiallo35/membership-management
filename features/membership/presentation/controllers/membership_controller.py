# TODO: Implement the MembershipController class
class MembershipService:
    pass


class MembershipController:
    def __init__(self, service: MembershipService):
        self.service = service

    async def create_membership(self): ...

    async def get_daily_membership(self): ...

    async def get_membership_by_id(self): ...

    async def get_memberships(self): ...

    async def update_membership(self): ...

    async def delete_membership(self): ...

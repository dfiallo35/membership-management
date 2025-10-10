from features.membership.domain.entities.membership import Membership
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)


class CreateMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self, membership: Membership) -> Membership:
        return await self.repository.save(membership)

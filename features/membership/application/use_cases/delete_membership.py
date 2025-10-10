from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.entities.membership import Membership


class DeleteMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self, membership_id: str) -> Membership:
        return await self.repository.delete(membership_id)

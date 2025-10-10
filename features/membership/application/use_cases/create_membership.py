from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)


class CreateMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self):
        return await self.repository.save()

from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.entities.membership import Membership


class ListMembershipsUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self) -> list[Membership]:
        return await self.repository.list(filters=MembershipFilters())

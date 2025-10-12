from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters


class DeleteMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self, membership_id: str) -> Membership:
        memberships = await self.repository.list(
            filters=MembershipFilters(
                id_eq=membership_id,
            )
        )
        if not memberships:
            raise ValueError("Membership not found")
        membership = memberships[0]

        memberships = await self.repository.list(
            filters=MembershipFilters(
                id_eq=membership_id,
                is_active=True,
            )
        )
        if not memberships:
            raise ValueError("Membership is active")

        return await self.repository.delete(membership)

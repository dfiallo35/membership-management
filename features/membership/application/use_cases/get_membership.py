from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.entities.membership import Membership
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
)


class GetMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self, membership_id: str) -> Membership:
        memberships = await self.repository.list(
            filters=MembershipFilters(id_eq=membership_id)
        )
        if not memberships:
            raise MembershipNotFoundError(membership_id)
        return memberships[0]

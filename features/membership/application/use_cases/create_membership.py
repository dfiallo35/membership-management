from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)


class CreateMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(self, membership: Membership) -> Membership:
        if membership.is_daily:
            memberships = await self.repository.list(
                filters=MembershipFilters(
                    gym_id_eq=membership.gym_id,
                    duration_days_eq=1,
                )
            )
            if memberships:
                raise ValueError("Already exists a daily membership")
        memberships = await self.repository.list(
            filters=MembershipFilters(
                gym_id_eq=membership.gym_id,
                name_eq=membership.name,
            )
        )
        if memberships:
            raise ValueError("Already exists a membership with the same name")

        return await self.repository.save(membership)

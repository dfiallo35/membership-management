from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.application.dtos.membership_dtos import MembershipUpdateRequest
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)


class UpdateMembershipUseCase:
    def __init__(self, repository: IMembershipRepository):
        self.repository = repository

    async def execute(
        self, membership_id: str, membership_update: MembershipUpdateRequest
    ) -> Membership:
        memberships = await self.repository.list(
            filters=MembershipFilters(
                id_eq=membership_id,
            )
        )
        if not memberships:
            raise ValueError("Membership not found")
        membership = memberships[0]

        if membership_update.name and membership.name != membership_update.name:
            memberships = await self.repository.list(
                filters=MembershipFilters(
                    name_eq=membership_update.name,
                    gym_id_eq=membership.gym_id,
                )
            )
            if memberships:
                raise ValueError("Membership already exists with the same name")
        if membership_update.duration_days == 1 and not membership.is_daily:
            memberships = await self.repository.list(
                filters=MembershipFilters(
                    duration_days_eq=1,
                    gym_id_eq=membership.gym_id,
                )
            )
            if memberships:
                raise ValueError("Daily membership already exists")

        membership_update_dict = membership_update.model_dump(exclude_unset=True)

        return await self.repository.update(membership, membership_update_dict)

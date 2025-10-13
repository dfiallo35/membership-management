from features.membership.domain.enums.logging_enums import LoggingModulesEnum
from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.application.dtos.membership_dtos import MembershipUpdateRequest
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.repository_interfaces.logging_repository import (
    ILoggingRepository,
)


class UpdateMembershipUseCase:
    def __init__(
        self, repository: IMembershipRepository, logging_repository: ILoggingRepository
    ):
        self.repository = repository
        self.logging_repository = logging_repository

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

        response = await self.repository.update(membership, membership_update_dict)

        await self.logging_repository.log_update(
            module_id=LoggingModulesEnum.MEMBERSHIP.value,
            gym_id=membership.gym_id,
            before_state=membership.model_dump(),
            after_state=response.model_dump(),
            description=f"Membership edited: {membership.name} -> {response.name}",
        )

        return response

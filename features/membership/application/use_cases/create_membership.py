from features.membership.domain.enums.logging_enums import LoggingModulesEnum
from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.repository_interfaces.logging_repository import (
    ILoggingRepository,
)


class CreateMembershipUseCase:
    def __init__(
        self, repository: IMembershipRepository, logging_repository: ILoggingRepository
    ):
        self.repository = repository
        self.logging_repository = logging_repository

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

        response = await self.repository.save(membership)

        await self.logging_repository.log_addition(
            module_id=LoggingModulesEnum.MEMBERSHIP.value,
            gym_id=membership.gym_id,
            before_state=None,
            after_state=membership.model_dump(),
            description=f"New membership: {membership.name} ({membership.duration_days} days)",
        )

        return response

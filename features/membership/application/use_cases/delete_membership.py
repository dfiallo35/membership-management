from features.membership.domain.enums.logging_enums import LoggingModulesEnum
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.repository_interfaces.logging_repository import (
    ILoggingRepository,
)
from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.application.errors.membership_errors import (
    MembershipNotFoundError,
    MembershipInUseError,
)


class DeleteMembershipUseCase:
    def __init__(
        self, repository: IMembershipRepository, logging_repository: ILoggingRepository
    ):
        self.repository = repository
        self.logging_repository = logging_repository

    async def execute(self, membership_id: str) -> Membership:
        memberships = await self.repository.list(
            filters=MembershipFilters(
                id_eq=membership_id,
            )
        )
        if not memberships:
            raise MembershipNotFoundError(membership_id)
        membership = memberships[0]

        memberships = await self.repository.list(
            filters=MembershipFilters(
                id_eq=membership_id,
                is_active=True,
            )
        )
        if not memberships:
            raise MembershipInUseError(membership_id)

        response = await self.repository.delete(membership)

        await self.logging_repository.log_deletion(
            module_id=LoggingModulesEnum.MEMBERSHIP.value,
            gym_id=membership.gym_id,
            before_state=membership.model_dump(),
            after_state=None,
            description=f"Membership deleted: {membership.name} ({membership.duration_days} days)",
        )

        return response

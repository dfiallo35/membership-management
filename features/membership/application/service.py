from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from features.membership.settings import Container
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.application.dtos.membership_dtos import (
    MembershipCreateRequest,
    MembershipPublic,
    MembershipUpdateRequest,
)
from features.membership.application.use_cases.create_membership import (
    CreateMembershipUseCase,
)
from features.membership.application.use_cases.delete_membership import (
    DeleteMembershipUseCase,
)
from features.membership.application.use_cases.get_membership import (
    GetMembershipUseCase,
)
from features.membership.application.use_cases.list_membership import (
    ListMembershipsUseCase,
)
from features.membership.application.use_cases.update_membership import (
    UpdateMembershipUseCase,
)
from features.membership.application.mappers.membership_mappers import MembershipMapper


class MembershipService:
    mapper = MembershipMapper()

    @inject
    def __init__(
        self,
        membership_repository: IMembershipRepository = Provide[
            Container.membership_repository
        ],
    ):
        self.membership_repository = membership_repository

    async def create_membership(
        self, membership: MembershipCreateRequest
    ) -> MembershipPublic:
        membership_entity = self.mapper.to_domain(membership)
        membership_response = await CreateMembershipUseCase(
            self.membership_repository
        ).execute(membership_entity)
        return self.mapper.to_response(membership_response)

    async def list_memberships(self) -> list[MembershipPublic]:
        memberships = await ListMembershipsUseCase(self.membership_repository).execute(
            filters=MembershipFilters()
        )
        return [self.mapper.to_response(membership) for membership in memberships]

    async def get_membership_by_id(self, membership_id: str) -> MembershipPublic:
        membership = await GetMembershipUseCase(self.membership_repository).execute(
            membership_id
        )
        return self.mapper.to_response(membership)

    async def update_membership(
        self, membership_id: str, membership_update: MembershipUpdateRequest
    ) -> MembershipPublic:
        membership_response = await UpdateMembershipUseCase(
            self.membership_repository
        ).execute(membership_id, membership_update)
        return self.mapper.to_response(membership_response)

    async def delete_membership(self, membership_id: str) -> None:
        return await DeleteMembershipUseCase(self.membership_repository).execute(
            membership_id
        )

    async def get_daily_membership(self) -> MembershipPublic | None:
        memberships = await ListMembershipsUseCase(self.membership_repository).execute(
            filters=MembershipFilters(duration_days_eq=1)
        )
        if not memberships:
            return None
        return self.mapper.to_response(memberships[0])

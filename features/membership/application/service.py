from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide


from features.membership.settings import Container
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)

from features.membership.application.dtos.membership_dtos import MembershipResponse
from features.membership.application.use_cases.create_membership import (
    CreateMembershipUseCase,
)
from features.membership.application.use_cases.list_membership import (
    ListMembershipsUseCase,
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

    async def create_membership(self):
        return await CreateMembershipUseCase(self.membership_repository).execute()

    async def list_memberships(self) -> list[MembershipResponse]:
        memberships = await ListMembershipsUseCase(self.membership_repository).execute()
        return [self.mapper.to_response(membership) for membership in memberships]

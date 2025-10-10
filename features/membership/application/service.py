from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide


from features.membership.settings import Container
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)

from features.membership.application.use_cases.create_membership import (
    CreateMembershipUseCase,
)


class MembershipService:
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

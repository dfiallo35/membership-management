from abc import ABC
from abc import abstractmethod

from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters


class IMembershipRepository(ABC):
    @abstractmethod
    async def save(self) -> None:
        pass

    @abstractmethod
    async def list(self, filters: MembershipFilters) -> list[Membership]:
        pass

    @abstractmethod
    async def delete(self) -> None:
        pass

    @abstractmethod
    async def update(self) -> None:
        pass

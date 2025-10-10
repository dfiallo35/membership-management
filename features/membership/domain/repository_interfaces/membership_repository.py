from abc import ABC
from abc import abstractmethod


class IMembershipRepository(ABC):
    @abstractmethod
    async def save(self) -> None:
        pass

    @abstractmethod
    async def find(self) -> None:
        pass

    @abstractmethod
    async def delete(self) -> None:
        pass

    @abstractmethod
    async def update(self) -> None:
        pass

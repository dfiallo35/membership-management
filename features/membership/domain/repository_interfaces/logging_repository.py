from abc import ABC
from abc import abstractmethod


class ILoggingRepository(ABC):
    @abstractmethod
    async def log_addition(self) -> None:
        pass

    @abstractmethod
    async def log_update(self) -> None:
        pass

    @abstractmethod
    async def log_deletion(self) -> None:
        pass

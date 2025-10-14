from features.membership.domain.repository_interfaces.logging_repository import (
    ILoggingRepository,
)
from features.membership.domain.enums.logging_enums import (
    LoggingOperationsEnum,
    LoggingModulesEnum,
)
from features.membership.infrastructure.entities.logging_model import LoggingModel
from features.membership.infrastructure.database.postgres import DbConnection


class LoggingRepositoryPostgres(ILoggingRepository):
    def __init__(self, db_connection: DbConnection):
        self.db_connection = db_connection

    async def _log(
        self,
        operation_id: str,
        module_id: str,
        gym_id: str,
        description: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> None:
        try:
            async with self.db_connection.get_session() as session:
                log = LoggingModel(
                    operation_id=operation_id,
                    module_id=module_id,
                    gym_id=gym_id,
                    before_state=before_state,
                    after_state=after_state,
                    description=description,
                )
                session.add(log)
                await session.commit()
        except Exception as e:
            raise e

    async def log_addition(
        self,
        module_id: LoggingModulesEnum,
        gym_id: str,
        description: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> None:
        await self._log(
            operation_id=LoggingOperationsEnum.ADDITION.value,
            module_id=module_id,
            gym_id=gym_id,
            before_state=before_state,
            after_state=after_state,
            description=description,
        )

    async def log_update(
        self,
        module_id: LoggingModulesEnum,
        gym_id: str,
        description: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> None:
        await self._log(
            operation_id=LoggingOperationsEnum.EDITION.value,
            module_id=module_id,
            gym_id=gym_id,
            before_state=before_state,
            after_state=after_state,
            description=description,
        )

    async def log_deletion(
        self,
        module_id: LoggingModulesEnum,
        gym_id: str,
        description: str,
        before_state: dict | None = None,
        after_state: dict | None = None,
    ) -> None:
        await self._log(
            operation_id=LoggingOperationsEnum.DELETION.value,
            module_id=module_id,
            gym_id=gym_id,
            before_state=before_state,
            after_state=after_state,
            description=description,
        )

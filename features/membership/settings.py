from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from pydantic_settings import BaseSettings


from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.domain.repository_interfaces.logging_repository import (
    ILoggingRepository,
)
from features.membership.infrastructure.repositories.membership_repository_postgres import (
    MembershipRepositoryPostgres,
)
from features.membership.infrastructure.repositories.logging_repository_postgres import (
    LoggingRepositoryPostgres,
)


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=["features.membership"],
    )

    config = providers.Configuration()

    db_connection = providers.Singleton(DbConnection, config.DATABASE_URL)

    membership_repository = providers.Singleton(
        MembershipRepositoryPostgres, db_connection=db_connection
    )
    logging_repository = providers.Singleton(
        LoggingRepositoryPostgres, db_connection=db_connection
    )

    repositories = providers.Dict(
        {
            IMembershipRepository: membership_repository,
            ILoggingRepository: logging_repository,
        }
    )


def create_container() -> Container:
    settings = Settings()
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()
    container.wire(modules=[__name__])
    return container

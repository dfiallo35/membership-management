from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from pydantic_settings import BaseSettings


from features.membership.infrastructure.database.postgres import DbConnection


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


def create_container() -> Container:
    settings = Settings()
    container = Container()
    container.config.from_pydantic(settings)
    return container

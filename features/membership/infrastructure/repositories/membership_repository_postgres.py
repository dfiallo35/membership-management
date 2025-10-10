from sqlalchemy import select

from features.membership.domain.entities.membership import Membership
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.infrastructure.mappers.membership_mappers import (
    MembershipMapper,
)
from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.infrastructure.entities.membership_model import MembershipModel
from features.membership.infrastructure.entities.membership_model import GymModel


class MembershipRepositoryPostgres(IMembershipRepository):
    mapper = MembershipMapper()

    def __init__(self, db_connection: DbConnection):
        self.db_connection = db_connection

    async def save(self):
        async with self.db_connection.get_session() as session:
            query = select(GymModel).where(GymModel.name == "Gym Test")
            gym = await session.execute(query)
            gym = gym.scalars().first()

            membership = MembershipModel(
                name="Membership Test",
                description="Description Test",
                duration_days=1,
                price=10,
                is_active=True,
                gym_id=gym.id,
            )
            session.add(membership)
            await session.commit()

    async def find(self) -> list[Membership]:
        async with self.db_connection.get_session() as session:
            query = select(MembershipModel)
            memberships = await session.execute(query)
            return [
                self.mapper.to_domain(membership)
                for membership in memberships.scalars().all()
            ]

    async def delete(self):
        pass

    async def update(self):
        pass

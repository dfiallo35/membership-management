from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.infrastructure.entities.membership_model import MembershipModel
from features.membership.infrastructure.entities.membership_model import GymModel


class MembershipRepositoryPostgres(IMembershipRepository):
    def __init__(self, db_connection: DbConnection):
        self.db_connection = db_connection

    async def save(self):
        async with self.db_connection.get_session() as session:
            gym = GymModel(name="Gym Test", memberships=[])
            session.add(gym)
            await session.commit()

            membership = MembershipModel(
                name="Membership Test",
                description="Description Test",
                duration_days=1,
                price=10,
                is_active=True,
                id_gym=gym.id,
            )
            session.add(membership)
            await session.commit()

    async def find(self):
        pass

    async def delete(self):
        pass

    async def update(self):
        pass

from sqlalchemy import select
from sqlalchemy.sql import Select

from features.membership.domain.entities.membership import Membership
from features.membership.domain.filters.membership_filters import MembershipFilters
from features.membership.domain.repository_interfaces.membership_repository import (
    IMembershipRepository,
)
from features.membership.infrastructure.mappers.membership_mappers import (
    MembershipMapper,
)
from features.membership.infrastructure.database.postgres import DbConnection
from features.membership.infrastructure.entities.membership_model import MembershipModel


class MembershipRepositoryPostgres(IMembershipRepository):
    mapper = MembershipMapper()

    def __init__(self, db_connection: DbConnection):
        self.db_connection = db_connection

    async def filter(self, filters: MembershipFilters, query: Select) -> Select:
        if filters.id_eq:
            query = query.where(MembershipModel.id == filters.id_eq)
        if filters.limit:
            query = query.limit(filters.limit)
        if filters.offset:
            query = query.offset(filters.offset)
        if filters.order_by:
            order_by = filters.order_by
            desc = order_by.startswith("-")
            order_by = order_by.lstrip("-")

            column = getattr(MembershipModel, order_by, None)
            if column:
                query = query.order_by(column.desc() if desc else column)

        return query

    async def save(self, membership: Membership):
        async with self.db_connection.get_session() as session:
            membership_model = self.mapper.to_model(membership)
            session.add(membership_model)
            await session.commit()
            await session.refresh(membership_model)
            return self.mapper.to_domain(membership_model)

    async def list(self, filters: MembershipFilters) -> list[Membership]:
        async with self.db_connection.get_session() as session:
            query = select(MembershipModel)
            query = await self.filter(filters, query)
            memberships = await session.execute(query)
            return [
                self.mapper.to_domain(membership)
                for membership in memberships.scalars().all()
            ]

    async def delete(self):
        pass

    async def update(self, membership_id: str, update_request: dict) -> Membership:
        async with self.db_connection.get_session() as session:
            membership_model = await session.get(MembershipModel, membership_id)
            if not membership_model:
                raise ValueError(f"Membership with id {membership_id} not found")

            for key, value in update_request.items():
                setattr(membership_model, key, value)
            await session.commit()
            await session.refresh(membership_model)
            return self.mapper.to_domain(membership_model)

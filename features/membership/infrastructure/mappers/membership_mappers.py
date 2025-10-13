from features.membership.domain.entities.membership import Membership
from features.membership.infrastructure.entities.membership_model import MembershipModel


class MembershipMapper:
    @staticmethod
    def to_model(membership: Membership) -> MembershipModel:
        return MembershipModel(**membership.model_dump())

    @staticmethod
    def to_domain(membership_model: MembershipModel) -> Membership:
        return Membership(
            id=str(membership_model.id),
            name=membership_model.name,
            description=membership_model.description,
            duration_days=membership_model.duration_days,
            price=membership_model.price,
            is_active=membership_model.is_active,
            gym_id=str(membership_model.gym_id),
        )

from features.membership.domain.entities.membership import Membership
from features.membership.application.dtos.membership_dtos import MembershipResponse


class MembershipMapper:
    @staticmethod
    def to_response(membership: Membership) -> MembershipResponse:
        return MembershipResponse(
            id=str(membership.id),
            name=membership.name,
            description=membership.description,
            duration_days=membership.duration_days,
            price=membership.price,
            is_active=membership.is_active,
            gym_id=str(membership.gym_id),
        )

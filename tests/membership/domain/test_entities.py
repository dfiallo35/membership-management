from uuid import uuid4
from schema import Schema

from features.membership.domain.entities.membership import Membership


def test_valid_membership():
    membership = Membership(
        id=str(uuid4()),
        name="Test",
        description="Test",
        duration_days=1,
        price=1,
        is_active=True,
        gym_id=str(uuid4()),
    )

    schema = Schema(
        {
            "id": str,
            "name": "Test",
            "description": "Test",
            "duration_days": 1,
            "price": 1,
            "is_active": True,
            "gym_id": str,
        }
    )

    assert schema.validate(membership.model_dump())

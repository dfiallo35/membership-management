from uuid import UUID
from pydantic import BaseModel


class Membership(BaseModel):
    id: UUID
    name: str
    description: str
    duration_days: int
    price: float
    is_active: bool
    gym_id: UUID

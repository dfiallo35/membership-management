from pydantic import BaseModel


class MembershipResponse(BaseModel):
    id: str
    name: str
    description: str
    duration_days: int
    price: float
    is_active: bool
    gym_id: str


class MembershipCreateRequest(BaseModel):
    name: str
    description: str
    duration_days: int
    price: float
    is_active: bool
    gym_id: str

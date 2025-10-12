from pydantic import BaseModel


class MembershipPublic(BaseModel):
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


class MembershipUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_days: int | None = None
    price: float | None = None
    is_active: bool | None = None

from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            UUID: str,
        }
    )


class Membership(BaseEntity):
    id: str
    name: str
    description: str
    duration_days: int
    price: float
    is_active: bool
    gym_id: str

    @property
    def is_daily(self) -> bool:
        return self.duration_days == 1

from pydantic import BaseModel
from pydantic import field_validator


class MembershipFilters(BaseModel):
    size: int | None = None
    page: int | None = None
    order_by: str | None = None

    id_eq: str | None = None
    duration_days_eq: int | None = None
    gym_id_eq: str | None = None
    name_eq: str | None = None
    is_active: bool | None = None

    @property
    def offset(self) -> int | None:
        if self.page is None or self.size is None:
            return None
        return (self.page) * self.size

    @property
    def limit(self) -> int | None:
        return self.size if self.size is not None else None

    @field_validator("id_eq", "gym_id_eq", mode="before")
    def field_id_to_str(cls, data: any) -> str | None:
        return str(data) if data is not None else None

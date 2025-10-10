from pydantic import BaseModel


class MembershipFilters(BaseModel):
    size: int | None = None
    page: int | None = None
    order_by: str | None = None

    id_eq: str | None = None

    @property
    def offset(self) -> int | None:
        if self.page is None or self.size is None:
            return None
        return (self.page) * self.size

    @property
    def limit(self) -> int | None:
        return self.size if self.size is not None else None

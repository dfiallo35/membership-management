from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from features.membership.infrastructure.entities.base_model import BaseModel
from features.membership.infrastructure.entities.gym_model import GymModel


class MembershipModel(BaseModel):
    __tablename__ = "membership"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    gym_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gym.id"), nullable=False
    )

    gym: Mapped[GymModel] = relationship("GymModel", back_populates="memberships")

from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from features.membership.infrastructure.entities.base_model import BaseModel


class GymModel(BaseModel):
    __tablename__ = "gym"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    memberships = relationship("MembershipModel", back_populates="gym")

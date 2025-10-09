from uuid import uuid4
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class GymModel(BaseModel):
    __tablename__ = "gym"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    memberships: Mapped[list["MembershipModel"]] = relationship(
        "MembershipModel", back_populates="gym"
    )


class MembershipModel(BaseModel):
    __tablename__ = "membership"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_gym: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gym.id"), nullable=False
    )

    gym: Mapped[GymModel] = relationship("GymModel", back_populates="memberships")

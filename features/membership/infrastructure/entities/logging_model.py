from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from features.membership.infrastructure.entities.base_model import BaseModel


class LoggingModel(BaseModel):
    __tablename__ = "logging"

    operation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    module_id: Mapped[str] = mapped_column(String(255), nullable=False)
    gym_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gym.id"), nullable=False
    )
    before_state: Mapped[dict] = mapped_column(JSON, nullable=True)
    after_state: Mapped[dict] = mapped_column(JSON, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

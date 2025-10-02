"""Model for deliveries"""

import uuid

from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case, extract

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel, DateTime, Enum, UUID

from backend.enums import DeliveryStatusEnum
from .job import Job


class Delivery(SQLModel, table=True):
    model_config = ConfigDict(ignored_types=(hybrid_property,))

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # unified fields
    ext_id: str = Field(nullable=False)  # "DEL-001-A" / "b-876543"
    supplier: str = Field(nullable=False)
    delivered_at: datetime = Field(
        DateTime(timezone=True), nullable=False
    )  # store in UTC
    status: DeliveryStatusEnum = Field(
        Enum(DeliveryStatusEnum, name="delivery_status", native_enum=False),
        nullable=False,
    )
    signed: bool = Field(nullable=False)

    source: str = Field(nullable=False)
    job_id: uuid.UUID = Field(
        UUID(as_uuid=True), foreign_key="jobs.id", nullable=False, ondelete="CASCADE"
    )

    job: Job = Relationship(back_populates="deliveries")

    @property
    def site_id(self) -> str:
        return self.job.site_id

    @hybrid_property
    def delivery_score(self) -> float:
        if self.signed:
            signed = 1.0
        else:
            signed = 0.3
        if 5 <= self.delivered_at.hour < 11:
            is_morning_delivery = 1.2
        else:
            is_morning_delivery = 1.0
        return signed * is_morning_delivery

    @delivery_score.expression
    def delivery_score(cls):
        signed_score = case((cls.signed == True, 1.0), else_=0.3) # noqa

        hour = extract("hour", cls.delivered_at)
        morning_score = case(((hour >= 5) & (hour < 11), 1.2), else_=1.0)
        return signed_score * morning_score

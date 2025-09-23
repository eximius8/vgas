"""Model for deliveries"""

import uuid
import enum
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel, DateTime, Enum, UUID

from .job import Job


class DeliveryStatus(str, enum.Enum):
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    PENDING = "pending"


class Source(str, enum.Enum):
    PARTNER_A = "partner_a"
    PARTNER_B = "partner_b"


class Delivery(SQLModel, table=True):

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # unified fields
    ext_id: str = Field(nullable=False)   # "DEL-001-A" / "b-876543"
    supplier: str = Field(nullable=False)
    delivered_at: datetime = Field(
        DateTime(timezone=True), nullable=False
    )  # store in UTC
    status: DeliveryStatus = Field(
        Enum(DeliveryStatus, name="delivery_status", native_enum=False),
        nullable=False
    )
    signed: bool = Field(nullable=False)
    site_id: str = Field(nullable=False)  # repeat for filtering

    source: Source = Field(
        Enum(Source, name="source_enum", native_enum=False),
        nullable=False
    )
    delivery_score: float = Field(nullable=False)
    job_id: uuid.UUID = Field(
        UUID(as_uuid=True), foreign_key="jobs.id", nullable=False, ondelete="CASCADE"
    )

    job: Job = Relationship(back_populates="deliveries")    

    def __repr__(self) -> str:
        return f"<Delivery job={self.job_id} ext_id={self.ext_id} status={self.status} score={self.delivery_score}>"

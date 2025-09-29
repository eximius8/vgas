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

    source: str = Field(nullable=False)
    job_id: uuid.UUID = Field(
        UUID(as_uuid=True), foreign_key="jobs.id", nullable=False, ondelete="CASCADE"
    )

    job: Job = Relationship(back_populates="deliveries")

    @property
    def site_id(self) -> str:
        return self.job.site_id

    @property
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


class DeliveryResponse(SQLModel):

    ext_id: str = Field(alias="id", schema_extra={"serialization_alias": "id"})
    supplier: str
    delivered_at: datetime = Field(alias="deliveredAt", schema_extra={"serialization_alias": "deliveredAt"})
    status: DeliveryStatus
    signed: bool
    site_id: str = Field(alias="siteId", schema_extra={"serialization_alias": "siteId"})
    source: str
    delivery_score: float = Field(alias="deliveryScore", schema_extra={"serialization_alias": "deliveryScore"})


class DeliveriesByJobResponse(SQLModel):
    job_id: uuid.UUID = Field(alias="jobId", schema_extra={"serialization_alias": "jobId"})
    items: list[DeliveryResponse] = Field(alias="deliveries")
    total: int
    limit: int
    offset: int
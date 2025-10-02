import uuid
from datetime import datetime
from pydantic import BaseModel, Field

from backend.enums import DeliveryStatusEnum


class DeliveryGetSerializer(BaseModel):
    ext_id: str = Field(serialization_alias="id")
    supplier: str
    delivered_at: datetime = Field(serialization_alias="deliveredAt")
    status: DeliveryStatusEnum
    signed: bool
    site_id: str = Field(serialization_alias="siteId")
    source: str
    delivery_score: float = Field(serialization_alias="deliveryScore")


class DeliveryListSerializer(BaseModel):
    job_id: uuid.UUID | None = Field(None, serialization_alias="jobId")
    items: list[DeliveryGetSerializer]
    total: int
    limit: int
    offset: int


import uuid
from datetime import datetime
from pydantic import BaseModel, Field

from backend.database.models.delivery import DeliveryStatus


class DeliveryResponse(BaseModel):

    ext_id: str = Field(serialization_alias="id")
    supplier: str
    delivered_at: datetime = Field(serialization_alias="deliveredAt")
    status: DeliveryStatus
    signed: bool
    site_id: str = Field(serialization_alias="siteId")
    source: str
    delivery_score: float = Field(serialization_alias="deliveryScore")


class DeliveriesResponse(BaseModel):

    job_id: uuid.UUID | None = Field(None, serialization_alias="jobId")
    items: list[DeliveryResponse]
    total: int
    limit: int
    offset: int

#class DeliveriesByJobResponse(DeliveriesResponse):
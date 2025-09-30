from datetime import datetime
from backend.enums import DeliveryStatus, SortByItems
from pydantic import BaseModel, Field


class DeliveryFilters(BaseModel):

    limit: int = 100
    offset: int = 0
    supplier: str | None = None
    status: DeliveryStatus | None = None
    signed: bool | None = None
    from_date: datetime | None = Field(None, alias="from")
    to_date: datetime | None = Field(None, alias="to")
    site_id: str | None = Field(None, alias="siteId")
    sort_by: SortByItems = Field(SortByItems.DELIVERY_SCORE_DESC, alias="sortBy")
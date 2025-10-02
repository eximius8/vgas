from datetime import datetime
from backend.enums import DeliveryStatusEnum, SortByItemsEnum
from pydantic import BaseModel, Field


class DeliveryFilter(BaseModel):

    limit: int = 100
    offset: int = 0
    supplier: str | None = None
    status: DeliveryStatusEnum | None = None
    signed: bool | None = None
    from_date: datetime | None = Field(None, alias="from")
    to_date: datetime | None = Field(None, alias="to")
    site_id: str | None = Field(None, alias="siteId")
    sort_by: SortByItemsEnum = Field(SortByItemsEnum.DELIVERY_SCORE_DESC, alias="sortBy")

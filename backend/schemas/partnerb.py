from datetime import datetime
from backend.database.models.delivery import DeliveryStatus
from pydantic import BaseModel, Field, computed_field


class ReceiverInfo(BaseModel):
    name: str
    signed: bool


class PartnerBDelivery(BaseModel):
    id: str = Field(serialization_alias='ext_id')
    provider: str = Field(serialization_alias='supplier')
    deliveredAt: datetime = Field(serialization_alias='delivered_at')
    statusCode: str = Field(exclude=True)
    receiver: ReceiverInfo | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def source(self) -> str:
        return "Partner B"

    @computed_field
    @property
    def status(self) -> str:
        status_map = {
            "OK": DeliveryStatus.DELIVERED.value,
            "FAILED": DeliveryStatus.CANCELLED.value,
        }
        return status_map.get(self.statusCode, DeliveryStatus.PENDING.value)

    @computed_field
    @property
    def signed(self) -> bool:
        if self.receiver is None:
            return False
        return self.receiver.signed

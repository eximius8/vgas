from datetime import datetime
from pydantic import BaseModel, Field, computed_field
from backend.enums import DeliveryStatusEnum


class DeliveryPartnerASerializer(BaseModel):
    deliveryId: str = Field(serialization_alias="ext_id")
    supplier: str
    timestamp: datetime = Field(serialization_alias="delivered_at")
    status: DeliveryStatusEnum
    signedBy: str | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def source(self) -> str:
        return "Partner A"

    @computed_field
    @property
    def signed(self) -> bool:
        return self.signedBy is not None


class ReceiverInfo(BaseModel):
    name: str
    signed: bool


class DeliveryPartnerBSerializer(BaseModel):
    id: str = Field(serialization_alias="ext_id")
    provider: str = Field(serialization_alias="supplier")
    deliveredAt: datetime = Field(serialization_alias="delivered_at")
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
            "OK": DeliveryStatusEnum.DELIVERED.value,
            "FAILED": DeliveryStatusEnum.CANCELLED.value,
        }
        return status_map.get(self.statusCode, DeliveryStatusEnum.PENDING.value)

    @computed_field
    @property
    def signed(self) -> bool:
        if self.receiver is None:
            return False
        return self.receiver.signed

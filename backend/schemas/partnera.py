from datetime import datetime
from backend.database.models.delivery import DeliveryStatus
from pydantic import BaseModel, Field, computed_field



# Partner A input schema
class PartnerADelivery(BaseModel):
    deliveryId: str = Field(serialization_alias='ext_id')
    supplier: str
    timestamp: datetime = Field(serialization_alias='delivered_at')
    status: DeliveryStatus
    signedBy: str | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def source(self) -> str:
        return "Partner A"

    @computed_field
    @property
    def signed(self) -> bool:
        return self.signedBy is not None

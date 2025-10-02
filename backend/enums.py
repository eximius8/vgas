import enum


class DeliveryStatusEnum(str, enum.Enum):
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    PENDING = "pending"


class JobStatusEnum(str, enum.Enum):
    CREATED = "created"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"


class SortByItemsEnum(str, enum.Enum):
    DELIVERED_AT_ASC = "delivered_at_asc"
    DELIVERED_AT_DESC = "delivered_at_desc"
    SUPPLIER_ASC = "supplier_asc"
    SUPPLIER_DESC = "supplier_desc"
    STATUS_ASC = "status_asc"
    STATUS_DESC = "status_desc"
    SOURCE_ASC = "source_asc"
    SOURCE_DESC = "source_desc"
    DELIVERY_SCORE_ASC = "delivery_score_asc"
    DELIVERY_SCORE_DESC = "delivery_score_desc"

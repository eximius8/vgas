import uuid
import logging
from sqlmodel import Session, select
from sqlalchemy import func, desc, asc

from backend.database import Delivery
from backend.schemas import PartnerADelivery, PartnerBDelivery
from backend.filters.deliveryfilter import DeliveryFilters
from backend.enums import SortByItems


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_deliveries_bulk(*, 
                         session: Session,
                         job_id: uuid.UUID,
                         deliveries: list[PartnerADelivery | PartnerBDelivery]) -> list[Delivery]:
    db_objs = []
    for delivery in deliveries:
        # Convert to dict and add job_id
        delivery_dict = delivery.model_dump(by_alias=True)
        delivery_dict['job_id'] = job_id
        
        # Now validate with the complete data
        db_obj = Delivery.model_validate(delivery_dict)
        db_objs.append(db_obj)
    
    session.add_all(db_objs)
    session.commit()
    for db_obj in db_objs:
        session.refresh(db_obj)
    return db_objs


def get_deliveries(
        *, 
        session: Session,
        job_id: uuid.UUID | None = None,
        filters: DeliveryFilters,
        ) -> dict:
    statement = select(Delivery)
    if job_id:
        statement = statement.where(Delivery.job_id == job_id)
    if filters.supplier:
        statement = statement.where(Delivery.supplier == filters.supplier)
    if filters.status:
        statement = statement.where(Delivery.status == filters.status)
    if filters.signed is not None:
        statement = statement.where(Delivery.signed == filters.signed)
    if filters.from_date:
        statement = statement.where(Delivery.delivered_at >= filters.from_date)
    if filters.to_date:
        statement = statement.where(Delivery.delivered_at <= filters.to_date)
    if filters.site_id:
        statement = statement.where(Delivery.site_id == filters.site_id)

    count_statement = select(func.count()).select_from(statement.subquery())
    total = session.exec(count_statement).one()

    sort_mapping = {
        SortByItems.DELIVERED_AT_ASC: asc(Delivery.delivered_at),
        SortByItems.DELIVERED_AT_DESC: desc(Delivery.delivered_at),
        SortByItems.SUPPLIER_ASC: asc(Delivery.supplier),
        SortByItems.SUPPLIER_DESC: desc(Delivery.supplier),
        SortByItems.STATUS_ASC: asc(Delivery.status),
        SortByItems.STATUS_DESC: desc(Delivery.status),
        SortByItems.SOURCE_ASC: asc(Delivery.source),
        SortByItems.SOURCE_DESC: desc(Delivery.source),
        SortByItems.DELIVERY_SCORE_ASC: asc(Delivery.delivery_score),
        SortByItems.DELIVERY_SCORE_DESC: desc(Delivery.delivery_score),
    }
    
    if filters.sort_by:
        statement = statement.order_by(sort_mapping[filters.sort_by])
    paginated_statement = statement.limit(filters.limit).offset(filters.offset)
    items = session.exec(paginated_statement).all()
    return {
        "items": items,
        "total": total
    }

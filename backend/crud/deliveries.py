import uuid
import logging
from sqlmodel import Session, select

from backend.database import Delivery
from backend.schemas import PartnerADelivery, PartnerBDelivery

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


def get_deliveries_by_job_id(*, session: Session, job_id: uuid.UUID) -> dict:
    statement = select(Delivery).where(Delivery.job_id == job_id)
    session_deliveries = session.exec(statement).all()
    return session_deliveries

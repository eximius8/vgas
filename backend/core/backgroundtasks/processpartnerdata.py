

import uuid

from backend.deps import SessionDep
import logging


from backend.core.crud import deliveries as deliveriescrud

from .serializers import DeliveryPartnerASerializer, DeliveryPartnerBSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



async def process_delivery(results: list | Exception, 
                            session: SessionDep, 
                            job_id: uuid.UUID,
                            schema: DeliveryPartnerASerializer | DeliveryPartnerBSerializer) -> None:
    """Process fetched results."""
    if isinstance(results, Exception):        
        return {'error': str(results)}
    deliveries = []
    stats = {"fetched": len(results), "transformed": 0, "errors": 0}
    for result in results:
        try:
            delivery = schema(**result)
            deliveries.append(delivery)
            stats["transformed"] += 1
        except Exception as e:
            logger.error(f"Error processing result {result}: {e}")
            stats["errors"] += 1
    if deliveries:
        deliveriescrud.create_deliveries_bulk(session=session, job_id=job_id, deliveries=deliveries)
    return stats


async def process_deliveries(partner_a_results: list, 
                             partner_b_results: list,
                             session: SessionDep, 
                             job_id: uuid.UUID) -> None:
    """Process deliveries from both partners."""
    stats_a = await process_delivery(partner_a_results, session, job_id, DeliveryPartnerASerializer)
    stats_b = await process_delivery(partner_b_results, session, job_id, DeliveryPartnerBSerializer)
    stored = stats_a.get('transformed', 0) + stats_b.get('transformed', 0)
    return {'partnerA': stats_a, 'partnerB': stats_b, 'stored': stored}

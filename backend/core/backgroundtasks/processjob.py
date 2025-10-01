
import uuid
from backend.enums import JobStatusEnum
from backend.deps import SessionDep
from backend.core.crud import jobs as jobscrud

from .fetchpartners import fetch_partners
from .processpartnerdata import process_deliveries


async def process_job(job_id: uuid.UUID, session: SessionDep) -> None:
    """
    Simulate fetching data from a partner URL.
    In a real implementation, this would involve making an HTTP request.
    Here, we just log the action and return True to indicate success.
    """
    jobscrud.update_job_status(
        session=session, job_id=job_id, status=JobStatusEnum.PROCESSING)

    partner_a_results, partner_b_results = await fetch_partners()

    stats = await process_deliveries(partner_a_results, partner_b_results, session, job_id)
    jobscrud.update_job_stats(
        session=session, job_id=job_id, stats=stats)
    if stats.get('stored', 0) > 0:
        jobscrud.update_job_status(
            session=session, job_id=job_id, status=JobStatusEnum.FINISHED)
    else:
        jobscrud.update_job_status(
            session=session, job_id=job_id, status=JobStatusEnum.FAILED)













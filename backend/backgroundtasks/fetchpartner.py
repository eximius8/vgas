import os
import uuid
import asyncio
import httpx

from backend.database import JobStatus
from backend.deps import SessionDep
from backend.crud import jobs as jobscrud

LOGISTICS_A_URL = os.getenv("LOGISTICS_A_URL", "http://mock_a:8000/api/logistics-a")
LOGISTICS_B_URL = os.getenv("LOGISTICS_B_URL", "http://mock_b:8000/api/logistics-b")


async def fetch_partner(partner_url: str) -> dict:
    """Fetch data from a partner URL."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(partner_url)
        response.raise_for_status()
        return response.json()


async def process_deliveries() -> bool:

    fetch_partner_a = fetch_partner(LOGISTICS_A_URL)
    fetch_partner_b = fetch_partner(LOGISTICS_B_URL)
    await asyncio.gather(fetch_partner_a, fetch_partner_b, return_exceptions=True)

    return True


async def process_job(job_id: uuid.UUID, session: SessionDep) -> None:
    """
    Simulate fetching data from a partner URL.
    In a real implementation, this would involve making an HTTP request.
    Here, we just log the action and return True to indicate success.
    """
    jobscrud.update_job_status(
        session=session, job_id=job_id, status=JobStatus.PROCESSING)

    is_data_fetched = await process_deliveries()
    if is_data_fetched:
        jobscrud.update_job_status(
            session=session, job_id=job_id, status=JobStatus.FINISHED)
    else:
        jobscrud.update_job_status(
            session=session, job_id=job_id, status=JobStatus.FAILED)

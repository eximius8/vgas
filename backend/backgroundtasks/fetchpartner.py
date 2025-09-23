import uuid
from backend.deps import SessionDep
from backend.crud import jobs as jobscrud


async def fetch_partner(partner_url: str) -> dict:
    """Fetch data from a partner URL."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(partner_url)
        response.raise_for_status()
        return response.json()


def process_job(job_id: uuid.UUID, session: SessionDep) -> bool:
    """
    Simulate fetching data from a partner URL.
    In a real implementation, this would involve making an HTTP request.
    Here, we just log the action and return True to indicate success.
    """
    job =jobscrud.get_job_by_id(session=session, job_id=job_id)
    job.status = "processing"
    session.add(job)
    session.commit()
    session.refresh(job)
    return True
    
import uuid
from backend.deps import SessionDep
from backend.crud import jobs as jobscrud


def fetch_partner(job_id: uuid.UUID, partner_url: str, session: SessionDep) -> bool:
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
    
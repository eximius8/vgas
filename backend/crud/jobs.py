import uuid
import logging
from sqlmodel import Session, select

from backend.database import Job, JobCreate, JobStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_job(*, session: Session, job_create: JobCreate) -> Job:
    db_obj = Job.model_validate(job_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_job_by_id(*, session: Session, job_id: uuid.UUID) -> Job | None:
    statement = select(Job).where(Job.id == job_id)
    session_job = session.exec(statement).first()
    return session_job


def update_job_status(*, session: Session, job_id: uuid.UUID, status: JobStatus) -> Job:
    
    session_job = get_job_by_id(session=session, job_id=job_id)
    if not session_job:
        logger.error(f"Job with id {job_id} not found.")

    session_job.status = status
    session.add(session_job)
    session.commit()
    session.refresh(session_job)
    return session_job

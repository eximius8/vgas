import uuid
from datetime import date
import logging
from sqlmodel import Session, select

from backend.enums import JobStatusEnum
from backend.core.database import Job
from backend.api.schemas.job import JobCreateSerializer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_job(*, session: Session, job_create: JobCreateSerializer) -> Job:
    db_obj = Job.model_validate(job_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_job_by_id(*, session: Session, job_id: uuid.UUID) -> Job | None:
    statement = select(Job).where(Job.id == job_id)
    session_job = session.exec(statement).first()
    return session_job


def get_job_by_site_id_date(*, session: Session, site_id: str, for_date: date) -> Job | None:
    statement = select(Job).where(Job.for_date == for_date).where(Job.site_id == site_id)
    session_job = session.exec(statement).first()
    if session_job and session_job.status in (JobStatusEnum.CREATED.value, JobStatusEnum.PROCESSING.value):
        return session_job


def update_job_status(*, session: Session, job_id: uuid.UUID, status: JobStatusEnum) -> Job | None:
    
    session_job = get_job_by_id(session=session, job_id=job_id)
    if not session_job:
        logger.error(f"Job with id {job_id} not found.")
        return None

    session_job.status = status
    session.add(session_job)
    session.commit()
    session.refresh(session_job)
    return session_job


def update_job_stats(*, session: Session, job_id: uuid.UUID, stats: dict) -> Job | None:
    
    session_job = get_job_by_id(session=session, job_id=job_id)
    if not session_job:
        logger.error(f"Job with id {job_id} not found.")
        return None

    session_job.stats = stats
    session.add(session_job)
    session.commit()
    session.refresh(session_job)
    return session_job
from sqlmodel import Session, select

from backend.database import Job, JobCreate


def create_job(*, session: Session, job_create: JobCreate) -> Job:
    db_obj = Job.model_validate(job_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_job_by_id(*, session: Session, job_id: str) -> Job | None:
    statement = select(Job).where(Job.id == job_id)
    session_job = session.exec(statement).first()
    return session_job

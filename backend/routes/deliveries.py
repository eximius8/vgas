from uuid import UUID
from typing import Any
from fastapi import APIRouter, BackgroundTasks, HTTPException
from backend.database import JobResponse, JobCreate, JobStatusResponse
from backend.deps import SessionDep
import backend.crud.jobs as jobscrud
from backend.backgroundtasks.fetchpartner import process_job

router = APIRouter(prefix="/backend/deliveries", tags=["deliveries"])


@router.post(
    "/fetch", response_model=JobResponse
)
def create_job(*, session: SessionDep, job_in: JobCreate, background_tasks: BackgroundTasks) -> Any:
    """
    Create new job.
    """
    job = jobscrud.create_job(session=session, job_create=job_in)
    job_response = JobResponse.model_validate(job)
    background_tasks.add_task(process_job, job.id, session)
    return job_response


@router.get(
    "/jobs/{job_id}", response_model=JobStatusResponse
)
def get_job(*, session: SessionDep, job_id: UUID) -> Any:
    """
    Get job status.
    """
    job = jobscrud.get_job_by_id(session=session, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_status_response = JobStatusResponse.model_validate(job)    
    return job_status_response

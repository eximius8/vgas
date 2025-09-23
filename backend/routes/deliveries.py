
from typing import Any
from fastapi import APIRouter
from backend.database import JobResponse, JobCreate
from backend.deps import SessionDep
import backend.crud.jobs as jobscrud

router = APIRouter(prefix="/backend/deliveries", tags=["deliveries"])


@router.post(
    "/fetch", response_model=JobResponse
)
def create_job(*, session: SessionDep, job_in: JobCreate) -> Any:
    """
    Create new job.
    """
    job = jobscrud.create_job(session=session, job_create=job_in)
    job_response = JobResponse.model_validate(job)
    return job_response

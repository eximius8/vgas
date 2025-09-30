from uuid import UUID
from typing import Any
from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, status
from backend.database import JobResponse, JobCreate, JobStatusResponse, DeliveryResponse, DeliveriesByJobResponse
from backend.deps import SessionDep
import backend.crud.jobs as jobscrud
import backend.crud.deliveries as deliveriescrud
from backend.backgroundtasks.processjob import process_job

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post(
    "/fetch", response_model=JobResponse
)
def create_job(*, 
               session: SessionDep, 
               job_in: JobCreate, 
               background_tasks: BackgroundTasks,
               response: Response) -> Any:
    """
    Create new job.
    """
    job = jobscrud.get_job_by_site_id_date(
        session=session, site_id=job_in.site_id, for_date=job_in.for_date)
    if job is None:
        job = jobscrud.create_job(session=session, job_create=job_in)
        background_tasks.add_task(process_job, job.id, session)
    else:
        response.status_code = status.HTTP_202_ACCEPTED
    job_response = JobResponse.model_validate(job)    
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


@router.get(
    "/jobs/{job_id}/results", response_model=DeliveriesByJobResponse
)
def get_job_results(*, session: SessionDep, job_id: UUID) -> Any:
    """
    Get job results.
    """
    deliveries = deliveriescrud.get_deliveries_by_job_id(session=session, job_id=job_id)

    response = DeliveriesByJobResponse(
        job_id=job_id,
        items=[DeliveryResponse.model_validate(delivery) for delivery in deliveries],
        total=len(deliveries),
        limit=len(deliveries),
        offset=0
    )
    return response
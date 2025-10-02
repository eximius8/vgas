from uuid import UUID
from typing import Any

from fastapi import (APIRouter, BackgroundTasks, 
                     HTTPException, Response, status, Depends)

from backend.deps import SessionDep

from backend.api.schemas import (JobGetSerializer, 
                                 JobCreateSerializer, 
                                 JobStatusSerializer,
                                 DeliveryGetSerializer,
                                 DeliveryListSerializer)

from backend.api.filters import DeliveryFilter

import backend.core.crud.jobs as jobscrud
import backend.core.crud.deliveries as deliveriescrud

from backend.core.backgroundtasks.processjob import process_job




router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post(
    "/fetch", response_model=JobGetSerializer, status_code=status.HTTP_202_ACCEPTED
)
def create_job(*, 
               session: SessionDep, 
               job_in: JobCreateSerializer, 
               background_tasks: BackgroundTasks,
               response: Response) -> Any:
    """
    Create new job.
    """
    created, job = jobscrud.get_or_create_job(
        session=session, job_create=job_in)
    if created:
        background_tasks.add_task(process_job, job.id, session)    
        response.status_code = status.HTTP_201_CREATED
    return job


@router.get(
    "/jobs/{job_id}", response_model=JobStatusSerializer
)
def get_job(*, session: SessionDep, job_id: UUID) -> Any:
    """
    Get job status.
    """
    job = jobscrud.get_job_by_id(session=session, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")  
    return job



@router.get(
    "/jobs/{job_id}/results", response_model=DeliveryListSerializer
)
def get_job_results(
        *, 
        session: SessionDep,
        job_id: UUID,
        filters: DeliveryFilter = Depends(),
    ) -> Any:
    """
    Get job results.
    """
    deliveries = deliveriescrud.get_deliveries(
        session=session, job_id=job_id, filters=filters)
    return {
        'job_id': job_id,
        'items': deliveries.get("items", []),
        'total': deliveries.get("total", 0),
        'limit': filters.limit,
        'offset': filters.offset
    }


@router.get(
    "/", response_model=DeliveryListSerializer, response_model_exclude_unset=True
)
def get_job_results(
        *, 
        session: SessionDep,
        filters: DeliveryFilter = Depends(),
    ) -> Any:
    """
    Get all results.
    """
    deliveries = deliveriescrud.get_deliveries(
        session=session, filters=filters)
    return {
        'items': deliveries.get("items", []),
        'total': deliveries.get("total", 0),
        'limit': filters.limit,
        'offset': filters.offset
    }
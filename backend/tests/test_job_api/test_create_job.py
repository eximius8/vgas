import pytest
from sqlmodel import Session
from httpx import AsyncClient, ASGITransport
from backend.deps import get_db
from backend.core.database import Job

from backend.api.schemas import JobCreateSerializer

from backend.enums import JobStatusEnum


from backend.main import app


@pytest.mark.asyncio
async def test_create_job(job_json):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/backend/deliveries/fetch", json=job_json)
    assert response.status_code == 201
    data = response.json()
    assert 'jobId' in data
    assert 'status' in data
    assert data['status'] == "created"


@pytest.mark.asyncio
@pytest.mark.parametrize('status', [JobStatusEnum.PROCESSING.value, JobStatusEnum.CREATED.value])
async def test_not_create_job_with_same_data_processing_created(job_json, session: Session, status: str):
    def get_session_override():
        return session  
    app.dependency_overrides[get_db] = get_session_override
    job_create = JobCreateSerializer(**job_json)
    job = Job.model_validate(job_create)
    job.status = status
    session.add(job)
    session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/backend/deliveries/fetch", json=job_json)        
    assert response.status_code == 202
    data = response.json()
    assert data['jobId'] == str(job.id)

@pytest.mark.asyncio
@pytest.mark.parametrize('status', [JobStatusEnum.FAILED.value, JobStatusEnum.FINISHED.value])
async def test_create_job_with_same_data_failed_finished(job_json, session: Session, status: str):
    def get_session_override():
        return session  
    app.dependency_overrides[get_db] = get_session_override
    job_create = JobCreateSerializer(**job_json)
    job = Job.model_validate(job_create)
    job.status = status
    session.add(job)
    session.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/backend/deliveries/fetch", json=job_json)        
    assert response.status_code == 201
    data = response.json()
    assert data['jobId'] != str(job.id)

import uuid
from datetime import date, datetime
import pytest

from sqlmodel import Session

from backend.core.database import Job
from backend.enums import JobStatusEnum


@pytest.fixture
def job_created() -> Job:
    """Basic job with minimal required fields"""
    return Job(
        id=uuid.uuid4(),
        site_id="TEST-001",
        for_date=date(2025, 10, 1),
        status=JobStatusEnum.CREATED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        stats={}
    )

@pytest.fixture
def job_processing() -> Job:
    """Job in completed status with stats"""
    return Job(
        id=uuid.uuid4(),
        site_id="TEST-002",
        for_date=date(2025, 10, 1),
        status=JobStatusEnum.PROCESSING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        stats={}
    )

@pytest.fixture
def job_finished() -> Job:
    """Job in completed status with stats"""
    return Job(
        id=uuid.uuid4(),
        site_id="TEST-002",
        for_date=date(2025, 10, 1),
        status=JobStatusEnum.FINISHED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        stats={
            "partnerA": { "fetched": 10, "transformed": 9, "errors": 1 },
            "partnerB": { "fetched": 7, "transformed": 7, "errors": 0 },
            "stored": 16
        }
    )

@pytest.fixture
def job_failed() -> Job:
    """Job in completed status with stats"""
    return Job(
        id=uuid.uuid4(),
        site_id="TEST-002",
        for_date=date(2025, 10, 1),
        status=JobStatusEnum.FAILED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        stats={
            "partnerA": 'Failed with error: ABC',
            "partnerB": { "fetched": 7, "transformed": 0, "errors": 7 },
            "stored": 0
        }
    )


@pytest.fixture
def sample_database_data(db_session: Session, job_created, 
                         job_processing, job_finished, job_failed):
    db_session.add_all([ job_created, job_processing, 
                        job_finished, job_failed])
    db_session.commit()


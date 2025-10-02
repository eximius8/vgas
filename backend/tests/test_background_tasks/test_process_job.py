import pytest
import os
from backend.core.backgroundtasks.processjob import process_job
import backend.core.backgroundtasks.fetchpartners
from backend.core.database import Job
from backend.enums import JobStatusEnum


@pytest.mark.asyncio
async def test_job_marked_failed(sample_database_data, db_session):
    job: Job = sample_database_data.get("created")
    await process_job(job.id, db_session)
    assert job.status == JobStatusEnum.FAILED


@pytest.mark.asyncio
async def test_job_marked_finished(
    sample_database_data,
    db_session,
    monkeypatch,
    partner_a_correct_response,
    partner_b_correct_response,
):
    async def fetch_partner(*args, **kwargs):
        return partner_a_correct_response + partner_b_correct_response

    monkeypatch.setattr(
        backend.core.backgroundtasks.fetchpartners, "fetch_partner", fetch_partner
    )
    job: Job = sample_database_data.get("created")
    await process_job(job.id, db_session)
    assert job.status == JobStatusEnum.FINISHED
    a_responses = len(partner_a_correct_response)
    b_responses = len(partner_b_correct_response)
    total_responses = a_responses + b_responses
    assert job.stats.get("stored") == total_responses
    assert job.stats.get("partnerA").get("errors") == b_responses
    assert job.stats.get("partnerB").get("errors") == a_responses
    assert job.stats.get("partnerA").get("fetched") == total_responses
    assert job.stats.get("partnerB").get("fetched") == total_responses
    assert job.stats.get("partnerA").get("transformed") == a_responses
    assert job.stats.get("partnerB").get("transformed") == b_responses


@pytest.mark.asyncio
async def test_job_marked_finished_no_data(
    sample_database_data, db_session, monkeypatch
):
    async def fetch_partner(*args, **kwargs):
        return []

    monkeypatch.setattr(
        backend.core.backgroundtasks.fetchpartners, "fetch_partner", fetch_partner
    )
    job: Job = sample_database_data.get("created")
    await process_job(job.id, db_session)
    assert job.status == JobStatusEnum.FINISHED

    assert job.stats.get("stored") == 0
    assert job.stats.get("partnerA").get("errors") == 0
    assert job.stats.get("partnerB").get("errors") == 0
    assert job.stats.get("partnerA").get("fetched") == 0
    assert job.stats.get("partnerB").get("fetched") == 0
    assert job.stats.get("partnerA").get("transformed") == 0
    assert job.stats.get("partnerB").get("transformed") == 0


@pytest.mark.asyncio
async def test_job_marked_finished_partial_success(
    sample_database_data, db_session, monkeypatch, partner_a_correct_response
):
    async def fetch_partner(*args, **kwargs):
        partner_a_url = os.getenv("LOGISTICS_A_URL")
        if args[0] == partner_a_url:
            return partner_a_correct_response
        raise Exception("Test exception")

    monkeypatch.setattr(
        backend.core.backgroundtasks.fetchpartners, "fetch_partner", fetch_partner
    )

    job: Job = sample_database_data.get("created")
    await process_job(job.id, db_session)
    assert job.status == JobStatusEnum.FINISHED
    assert job.stats.get("stored") == len(partner_a_correct_response)
    assert job.stats.get("partnerA").get("errors") == 0
    assert job.stats.get("partnerA").get("fetched") == len(partner_a_correct_response)
    assert job.stats.get("partnerA").get("transformed") == len(
        partner_a_correct_response
    )
    assert job.stats.get("partnerB").get("error") == "Test exception"

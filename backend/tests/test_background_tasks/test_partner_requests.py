import pytest
from backend.core.backgroundtasks.fetchpartners import fetch_partners
import backend.core.backgroundtasks.fetchpartners




@pytest.mark.asyncio
async def test_exception_returned():

    results = await fetch_partners()

    assert len(results) == 2
    assert isinstance(results[0], Exception)
    assert isinstance(results[1], Exception)


@pytest.mark.asyncio
async def test_partners_available(monkeypatch, partner_a_correct_response, partner_b_correct_response):
    async def fetch_partner(*args, **kwargs):
        return partner_a_correct_response + partner_b_correct_response
    
    monkeypatch.setattr(
        backend.core.backgroundtasks.fetchpartners, 
        "fetch_partner", 
        fetch_partner
    )

    results = await fetch_partners()
    assert len(results) == 2
    assert isinstance(results[0], list)
    assert isinstance(results[1], list)

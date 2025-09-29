
from typing import List
import asyncio
import httpx

from backend.settings import LOGISTICS_A_URL, LOGISTICS_B_URL


async def fetch_partner(partner_url: str) -> List[dict]:
    """Fetch data from a partner URL."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(partner_url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError(f"Expected list from {partner_url}, got {type(data)}")
        return data
    

async def fetch_partners() -> List[List[dict] | Exception]:

    fetch_partner_a = fetch_partner(LOGISTICS_A_URL)
    fetch_partner_b = fetch_partner(LOGISTICS_B_URL)
    partner_a_results, partner_b_results = await asyncio.gather(fetch_partner_a, fetch_partner_b, return_exceptions=True)
    
    return [partner_a_results, partner_b_results]


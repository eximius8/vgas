
from typing import List
import asyncio
import logging
import httpx

from backend.settings import LOGISTICS_A_URL, LOGISTICS_B_URL

logger = logging.getLogger(__name__)


async def fetch_partner(partner_url: str, timeout: float = 5.0) -> List[dict]:
    """Fetch data from a partner URL."""
    async with httpx.AsyncClient() as client:
        try:
            logger.debug(f'Fetching {partner_url}')
            response = await client.post(partner_url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError(f"Expected list from {partner_url}, got {type(data)}: {data}")
            return data
        except httpx.TimeoutException as e:
            logger.error(f'Timeout error fetching {partner_url}: {e}')
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f'HTTP status error fetching {partner_url}: {e.response.status_code} - {e}')
            raise
        except httpx.RequestError as e:
            logger.error(f'Request error fetching {partner_url}: {e}')
            raise
        except Exception as e:
            logger.error(f'Unexpected error fetching {partner_url}: {e}')
            raise
    

async def fetch_partners() -> List[List[dict] | Exception]:

    fetch_partner_a = fetch_partner(LOGISTICS_A_URL)
    fetch_partner_b = fetch_partner(LOGISTICS_B_URL)
    partner_a_results, partner_b_results = await asyncio.gather(fetch_partner_a, fetch_partner_b, return_exceptions=True)
    
    return [partner_a_results, partner_b_results]


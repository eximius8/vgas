import logging

import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.api.routes import deliveriesrouter
from backend.settings import LOGISTICS_A_URL, LOGISTICS_B_URL

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Check Partner A
        try:
            r = await client.post(LOGISTICS_A_URL)
            if r.status_code == 200:
                logger.info(f"Partner A reachable at {LOGISTICS_A_URL}")
            else:
                logger.error(
                    f"Partner A returned status {r.status_code} at {LOGISTICS_A_URL}"
                )
        except Exception as e:
            logger.error(f"Failed to reach Partner A at {LOGISTICS_A_URL}: {e}")

        # Check Partner B
        try:
            r = await client.post(LOGISTICS_B_URL)
            if r.status_code == 200:
                logger.info(f"Partner B reachable at {LOGISTICS_B_URL}")
            else:
                logger.error(
                    f"Partner B returned status {r.status_code} at {LOGISTICS_B_URL}"
                )
        except Exception as e:
            logger.error(f"Failed to reach Partner B at {LOGISTICS_B_URL}: {e}")

    yield

    logger.info("Application shutdown complete.")


app = FastAPI(
    title="VESTIGAS Backend Challenge", lifespan=lifespan, root_path="/backend"
)

app.include_router(deliveriesrouter.router)


@app.get("/")
def root():
    return {"message": "Backend challenge scaffold is running"}

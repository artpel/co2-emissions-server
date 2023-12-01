from fastapi import FastAPI
from app.api.v1 import get_co2_emissions
from app.core.config import config
import uvicorn

app = FastAPI()

app.include_router(get_co2_emissions.router, prefix="/v1", tags=["v1"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=config.API_PORT)

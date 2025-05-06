from fastapi import APIRouter
from pydantic import BaseModel
import os
import psutil
import time
import logging

router = APIRouter()
logger = logging.getLogger("api")


class HealthStatus(BaseModel):
    status: str
    version: str
    uptime: float
    memory_usage: float
    cpu_usage: float


start_time = time.time()
version = os.getenv("VERSION", "0.1.0")


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint to monitor service status.
    Returns basic metrics about the service.
    """
    uptime = time.time() - start_time
    memory_info = psutil.Process().memory_info()

    health_data = HealthStatus(
        status="ok",
        version=version,
        uptime=uptime,
        memory_usage=memory_info.rss / (1024 * 1024),  # MB
        cpu_usage=psutil.cpu_percent(),
    )

    logger.info(f"Health check performed: {health_data}")
    return health_data


@router.get("/readiness")
async def readiness():
    """
    Readiness probe for Kubernetes.
    Returns 200 OK when the service is ready to accept requests.
    """
    return {"status": "ready"}


@router.get("/liveness")
async def liveness():
    """
    Liveness probe for Kubernetes.
    Returns 200 OK when the service is alive.
    """
    return {"status": "alive"}

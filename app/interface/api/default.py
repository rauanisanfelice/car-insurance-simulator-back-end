from datetime import datetime, timezone

from fastapi import APIRouter

start_time = datetime.now(tz=timezone.utc)

router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:
    uptime = datetime.now(tz=timezone.utc) - start_time
    return {"message": "pong", "runningTime": str(uptime)}


@router.get("/health")
async def health() -> dict[str, str]:
    return {"message": "I'm alive and kicking!"}

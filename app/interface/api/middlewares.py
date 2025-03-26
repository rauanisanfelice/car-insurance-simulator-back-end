from fastapi import Request
from fastapi.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/", "/health", "/ping", "/health/", "/ping/"}:
            return await call_next(request)

        logger.info("method: %s, url: %s", request.method, request.url)
        logger.debug("Request: %s", request.__dict__)

        return await call_next(request)

from typing import Any

from app.config import settings
from app.shared.models import EntityModel


class ApiError(EntityModel):
    developer_message: str | None = None
    user_message: str | None = None
    error_code: int | None = 1000
    more_info: str | None = settings.API_ERROR_MORE_INFO


class RequestValidationApiError(ApiError):
    errors: Any

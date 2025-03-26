from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.infrastructure.services.logging import logger
from app.interface.api.error_schema import ApiError, RequestValidationApiError


def init(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        request_validation_error = RequestValidationApiError(
            developer_message=str(exc),
            errors=exc.errors(),
        )
        request_validation_error_dict = request_validation_error.model_dump()

        log_extra = {
            "request_validation_error": request_validation_error_dict,
            "request": {"method": request.method, "path": request.url.path},
        }
        logger.exception(request_validation_error.developer_message, extra=log_extra)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(request_validation_error_dict),
        )

    @app.exception_handler(Exception)
    def default_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        api_error = ApiError(developer_message=str(exc))
        api_error_dict = api_error.model_dump()

        log_extra = {
            "api_error": api_error_dict,
            "request": {"method": request.method, "path": request.url.path},
        }
        logger.exception(api_error.developer_message, extra=log_extra)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=api_error_dict,
        )

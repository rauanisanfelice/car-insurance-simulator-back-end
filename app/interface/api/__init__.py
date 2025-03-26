from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.interface.api.default import router as default_router
from app.interface.api.error_handling import init as init_error_handling
from app.interface.api.middlewares import LoggingMiddleware
from app.interface.api.v1 import api as api_v1
from app.shared.version import VERSION


def create_app():
    external_docs = {
        "description": "GitHub",
        "url": settings.API_ERROR_MORE_INFO,
    }
    tags_metadata = [
        {
            "name": "insurance",
            "description": "Operations related to insurance",
            "externalDocs": external_docs,
        },
        {
            "name": "default",
            "description": "Operations related to default",
            "externalDocs": external_docs,
        },
    ]
    description = "This is the API for the Car Insurance Simulator."

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version=VERSION,
        openapi_tags=tags_metadata,
        contact={
            "name": "Rauan Sanfelice",
            "url": "https://github.com/rauanisanfelice",
            "email": "rauan.sanfelice@gmail.com",
        },
    )

    # Error handling
    init_error_handling(app)

    # Middlewares
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Define routers
    app.include_router(default_router)
    app.include_router(api_v1.router, prefix=settings.API_V1_STR)

    return app

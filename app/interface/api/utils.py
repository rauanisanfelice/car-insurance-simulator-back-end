import secrets
import string
from typing import Any

from fastapi.requests import Request


def generate_request_id() -> str:
    return "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6)
    )


def url_for(
    request: Request,
    name: str,
    query_parameters: dict[Any, Any],
    args: dict[Any, Any] | None = None,
) -> str:
    args = args or {}
    url = request.url_for(name, **args)
    parameters = [f"{key}={value}" for key, value in query_parameters.items()]
    return str(url) + "?" + "&".join(parameters)

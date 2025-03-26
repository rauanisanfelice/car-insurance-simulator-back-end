import json

from fastapi import status


class TestEndpointsDefault:
    def test_router_ping(self, client_test_default) -> None:
        response = client_test_default.get("/ping")
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["message"] == "pong"

    def test_router_health(self, client_test_default) -> None:
        response = client_test_default.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["message"] == "I'm alive and kicking!"

    def test_error_router(self, client_test_default) -> None:
        response = client_test_default.get("/pings")
        assert response.status_code == status.HTTP_404_NOT_FOUND

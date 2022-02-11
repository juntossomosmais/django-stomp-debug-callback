import requests

from django_template import settings


class TestMiddlewares:
    def test_liveness_is_properly_configured(self, live_server):
        # Arrange
        liveness_url_value = settings.LIVENESS_URL
        address = f"{live_server.url}{liveness_url_value}"
        # Act
        response = requests.get(address)
        # Assert
        assert response.status_code == 200
        body = response.json()
        assert body == {"message": "Ok"}
        middlewares = settings.MIDDLEWARE
        is_it_first_middleware = middlewares[0] == "django_template.support.middleware.LivenessHealthCheckMiddleware"
        assert is_it_first_middleware

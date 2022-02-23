import os
import uuid

from django.conf import settings

pytest_plugins = ["tests.client_conftest"]


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=["django_stomp", "django_stomp_debug_callback"],
        ROOT_URLCONF="django_stomp_debug_callback.urls",
        DATABASES={
            "default": {
                "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
                "NAME": os.getenv("DB_DATABASE", f"test_db-{uuid.uuid4()}"),
                "USER": os.getenv("DB_USER"),
                "HOST": os.getenv("DB_HOST"),
                "PORT": os.getenv("DB_PORT"),
                "PASSWORD": os.getenv("DB_PASSWORD"),
                "TEST": {"NAME": os.getenv("DB_DATABASE", f"test_db-{uuid.uuid4()}")},
            }
        },
        SECRET_KEY=uuid.uuid4(),
    )

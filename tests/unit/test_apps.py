from django.apps import apps
from django.test import TestCase
from django_stomp_debug_callback.apps import DjangoStompDebugCallback


class TestDjangoStompDebugCallback(TestCase):
    def test_apps(self):
        self.assertEqual(DjangoStompDebugCallback.name, 'django_stomp_debug_callback')
        self.assertEqual(apps.get_app_config('django_stomp_debug_callback').name, 'django_stomp_debug_callback')
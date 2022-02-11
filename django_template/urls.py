from django.contrib import admin
from django.urls import include
from django.urls import path

from django_template.apps.example.api.v1 import standard_views as standard_views_v1

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("healthcheck/readiness", include("health_check.urls"), name="health-check"),
    path("api/v1/users/attributes", standard_views_v1.UserManagementAttributesAPIView.as_view()),
]

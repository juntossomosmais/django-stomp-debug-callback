import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_template.apps.example.api.v1.serializers import UserAttributesSerializer
from django_template.apps.example.models import AuditAction

_logger = logging.getLogger(__name__)


class UserManagementAttributesAPIView(APIView):
    def post(self, request):
        user_id = "123456qwerty"
        _logger.debug("The following user is trying to refresh his attributes: %s", user_id)
        serializer = UserAttributesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _logger.info("What I received: %s", serializer.validated_data)

        AuditAction(user_id=user_id, action=UserManagementAttributesAPIView.post.__name__, success=True).save()

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user_id = "Salted User has been logged"
        _logger.debug("The following user is trying to retrieve his attributes: %s", user_id)
        body = {
            "full_name": "Carl Edward Sagan",
            "given_name": "Carl",
            "family_name": "Sagan",
            "user_metadata": {
                "Fields": [
                    "Astronomy",
                    "Astrophysics",
                    "Cosmology",
                    "Astrobiology",
                    "Space science",
                    "Planetary science",
                ],
                "Institutions": [
                    "University of Chicago",
                    "Cornell University",
                    "Harvard University",
                    "Smithsonian Astrophysical Observatory",
                    "University of California, Berkeley",
                ],
            },
        }
        return Response(body, status=status.HTTP_200_OK)

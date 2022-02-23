import importlib
import json
import logging

from http import HTTPStatus

from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_stomp.services.consumer import Payload

from django_stomp_debug_callback.utils import mock_callable_function

_logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@csrf_exempt
def debug_callback_view(request: HttpRequest) -> JsonResponse:
    """
    View wrapper to call pubsub logic

    Request Body:
    ```
        {
            "callback_function_path": "path.to.your.function",
            "payload_body": {
                "user_id_ref": "0c2b3b31-6b98-426b-93d1-fb4b97038e23"
            },
            "payload_headers": {
                "fake": "headers"
            }
        }
    ```
    """
    _logger.info("What I received: %s", request.body)
    request_body = json.loads(request.body)

    callback_function_path = request_body.get("callback_function_path") or None
    if not callback_function_path:
        return JsonResponse(
            status=HTTPStatus.BAD_REQUEST,
            data={"detail": "callback_function_path is required"},
        )

    callback_function_name = callback_function_path.split(".")[-1]
    callback_module_path = ".".join(callback_function_path.split(".")[0:-1])

    payload_body = request_body.get("payload_body") or {}
    payload_headers = request_body.get("payload_headers") or {}
    fake_payload = Payload(mock_callable_function, mock_callable_function, payload_headers, payload_body)

    callback_function = importlib.import_module(callback_module_path)
    callback_function_to_call = getattr(callback_function, callback_function_name)

    _logger.debug("Calling %s from module %s", callback_function_name, callback_module_path)

    callback_function_to_call(fake_payload)

    return JsonResponse({"detail": "OK"})

import json

from http import HTTPStatus

import pytest

from django.http import HttpRequest
from django_stomp.services.consumer import Payload
from pytest_mock import MockerFixture

from django_stomp_debug_callback.views import debug_callback_view
from django_stomp_debug_callback.views import mock_callable_function
from tests.utils import fake_body
from tests.utils import fake_callback_path
from tests.utils import fake_headers


def test_should_call_callback_command_function(mocker: MockerFixture) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    mock_request = HttpRequest()
    mock_request.method = "POST"
    mock_request._body = json.dumps(
        {
            "callback_function_path": fake_callback_path,
            "payload_body": fake_body,
            "payload_headers": fake_headers,
        }
    )
    debug_callback_view(mock_request)
    mock_fake_callback_function.assert_called_once_with(
        (
            Payload(
                ack=mock_callable_function,
                nack=mock_callable_function,
                body=fake_body,
                headers=fake_headers,
            )
        )
    )


def test_should_return_error_when_method_not_is_post(mocker: MockerFixture) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    mock_request = HttpRequest()
    mock_request.method = "GET"

    response = debug_callback_view(mock_request)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    mock_fake_callback_function.assert_not_called()


def test_should_return_error_when_callback_function_path_body_attribute_is_not_provided(mocker: MockerFixture) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    mock_request = HttpRequest()
    mock_request.method = "POST"
    mock_request._body = json.dumps({})  # empty body

    response = debug_callback_view(mock_request)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.content == b'{"detail": "callback_function_path is required"}'

    mock_fake_callback_function.assert_not_called()


def test_should_raise_when_callback_function_launch_error(mocker: MockerFixture) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)
    mock_fake_callback_function.side_effect = Exception(":careca:")

    mock_request = HttpRequest()
    mock_request.method = "POST"
    mock_request._body = json.dumps(
        {
            "callback_function_path": fake_callback_path,
            "payload_body": fake_body,
            "payload_headers": fake_headers,
        }
    )

    # serializer invocation
    with pytest.raises(Exception):
        debug_callback_view(mock_request)

        mock_fake_callback_function.assert_called_once_with(
            (
                Payload(
                    ack=mock_callable_function,
                    nack=mock_callable_function,
                    body=fake_body,
                    headers=fake_headers,
                )
            )
        )


def test_should_return_ok_when_callback_function_not_raise_error(mocker: MockerFixture) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    mock_request = HttpRequest()
    mock_request.method = "POST"
    mock_request._body = json.dumps(
        {
            "callback_function_path": fake_callback_path,
            "payload_body": fake_body,
            "payload_headers": fake_headers,
        }
    )

    response = debug_callback_view(mock_request)

    assert response.status_code == HTTPStatus.OK
    assert response.content == b'{"detail": "OK"}'

    mock_fake_callback_function.assert_called_once_with(
        (
            Payload(
                ack=mock_callable_function,
                nack=mock_callable_function,
                body=fake_body,
                headers=fake_headers,
            )
        )
    )

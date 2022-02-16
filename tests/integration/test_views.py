import json

from http import HTTPStatus

import pytest

from django.test.client import Client
from django.urls import reverse
from django_stomp.services.consumer import Payload
from pytest_mock import MockerFixture

from django_stomp_debug_callback.utils import mock_callable_function
from tests.utils import fake_body
from tests.utils import fake_callback_path
from tests.utils import fake_headers

endpoint_url = reverse("debug-callback-view")


def test_should_call_callback_command_function(mocker: MockerFixture, client_request: Client) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    request_body = {
        "callback_function_path": fake_callback_path,
        "payload_body": fake_body,
        "payload_headers": fake_headers,
    }
    response = client_request.post(endpoint_url, data=request_body, content_type="application/json")

    assert response.status_code == HTTPStatus.OK
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


def test_should_return_error_when_method_not_is_post(mocker: MockerFixture, client_request: Client) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)
    response = client_request.get(endpoint_url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    mock_fake_callback_function.assert_not_called()


def test_should_return_error_when_callback_function_path_body_attribute_is_not_provided(
    mocker: MockerFixture, client_request: Client
) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    body = {}  # empty body
    response = client_request.post(endpoint_url, data=body, content_type="application/json")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.content == b'{"detail": "callback_function_path is required"}'
    mock_fake_callback_function.assert_not_called()


def test_should_return_warning_when_callback_function_raise_error(
    mocker: MockerFixture, client_request: Client
) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)
    mock_fake_callback_function.side_effect = Exception(":careca:")

    request_body = json.dumps(
        {
            "callback_function_path": fake_callback_path,
            "payload_body": fake_body,
            "payload_headers": fake_headers,
        }
    )

    with pytest.raises(Exception):
        client_request.post(endpoint_url, data=request_body, content_type="application/json")

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


def test_should_return_ok_when_callback_function_not_raise_error(mocker: MockerFixture, client_request: Client) -> None:
    mock_fake_callback_function = mocker.patch(fake_callback_path)

    request_body = {
        "callback_function_path": fake_callback_path,
        "payload_body": fake_body,
        "payload_headers": fake_headers,
    }
    response = client_request.post(endpoint_url, data=request_body, content_type="application/json")

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

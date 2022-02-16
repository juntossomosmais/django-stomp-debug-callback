from django_stomp_debug_callback.utils import mock_callable_function


def test_should_mock_callable_function_return_none() -> None:
    assert mock_callable_function() is None

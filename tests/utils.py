from django_stomp.services.consumer import Payload

fake_callback_path = "tests.utils.fake_callback"
fake_body = {"fake": "body"}
fake_headers = {"fake": "headers"}


def fake_callback(payload: Payload):
    return

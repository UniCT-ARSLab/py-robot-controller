import requests

from models.constants import HEALTHCHECK_MESSAGE


def test_healthcheck() -> None:
    r = requests.get("http://localhost:5000/healthcheck")
    assert r.text == HEALTHCHECK_MESSAGE

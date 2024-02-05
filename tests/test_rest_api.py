import requests

from models.constants import HEALTHCHECK_MESSAGE


def test_healthcheck() -> None:
    r = requests.get("http://localhost:5000/healthcheck", timeout=10)
    assert r.text == HEALTHCHECK_MESSAGE

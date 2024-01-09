from webserver.example import ex


def test_ex() -> None:
    assert ex(3, 4) == 7

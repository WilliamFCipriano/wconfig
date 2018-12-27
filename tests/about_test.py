import pytest


def test():
    y = pytest.importorskip("wconfig.about")
    x = y._()
    x = y._(f=False)
    assert x == y.__doc__






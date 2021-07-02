import pytest
from goat.api import API


@pytest.fixture
def api():
    return API()


def url(s):
    return f"http://testserver{s}"


@pytest.fixture
def client(api):
    return api.test_session()

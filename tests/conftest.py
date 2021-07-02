import pytest
import goat


@pytest.fixture
def app():
    return goat.Goat()


def url(s):
    return f"http://testserver{s}"


@pytest.fixture
def client(app):
    return app.test_session()

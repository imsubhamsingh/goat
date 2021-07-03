import pytest

from goat.utils.tests import url


def test_class_based_handler_get(app, client):
    response_text = "This is a get request"

    @app.route("/food")
    class FoodResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get(url("/food")).text == response_text


def test_class_based_handler_post(app, client):
    response_text = "This is a post request"

    @app.route("/food")
    class FoodResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post(url("/food")).text == response_text


def test_class_based_handler_not_allowed_method(app, client):
    @app.route("/food")
    class FoodResource:
        def post(self, req, resp):
            resp.text = "goat"

    with pytest.raises(AttributeError):
        client.get(url("/food"))

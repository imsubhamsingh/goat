import pytest

from goat.utils.tests import url


def test_basic_route(app):
    @app.route("/home")
    def home(req, resp):
        resp.body = "YOO"


def test_route_overlap_throws_exception(app):
    @app.route("/home")
    def home(req, resp):
        resp.body = "YOO"

    with pytest.raises(AssertionError):

        @app.route("/home")
        def home2(req, resp):
            resp.body = "YOO"


def test_alternate_route(app, client):
    response_text = "Alternate or django way to add a route."

    def home(req, resp):
        resp.body = response_text

    app.add_route("/alternative", home)

    assert client.get(url("/alternative")).text == response_text


def test_alternative_route_overlap_throws_exception(app):
    def home(req, resp):
        resp.body = "Welcome Django."

    def home2(req, resp):
        resp.body = "Welcome Goat"

    app.add_route("/alternative", home)

    with pytest.raises(AssertionError):
        app.add_route("/alternative", home2)


def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.body = f"hey {name}!"

    assert client.get("http://testserver/subham").text == "hey subham!"
    assert client.get("http://testserver/singh").text == "hey singh!"


def test_class_based_handler_route_registration(app):
    @app.route("/food")
    class Framework:
        def get(self, req, resp):
            resp.body = "goat"

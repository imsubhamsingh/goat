import pytest
from goat import Goat
from goat.requests import Request
from goat.responses import Response


def url(s):
    return f"http://testserver{s}"


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


def test_goat_test_client_can_send_request(app, client):
    RESPONSE_TEXT = "THIS IS A MESSAGE FOR YOU"

    @app.route("/hey")
    def cool(req, resp):
        resp.body = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.body = f"hey {name}!"

    assert client.get("http://testserver/subham").text == "hey subham!"
    assert client.get("http://testserver/singh").text == "hey singh!"


def test_default_404_response(app, client):
    response = client.get("http://testserver/notfound")

    assert response.status_code == 404
    assert response.text == "Sorry, page not Found."


def test_status_code_returned(app, client):
    @app.route("/xxx")
    def xxx(req, resp):
        resp.body = "not xxx things ;)"
        resp.status_code = 215

    assert client.get(url("/xxx")).status_code == 215


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

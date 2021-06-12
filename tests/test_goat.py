import pytest
from api import API
from webob import Request, Response


@pytest.fixture
def api():
    return API()


def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOO"


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOO"

    with pytest.raises(AssertionError):

        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOO"

from goat.utils.tests import url


def test_json_response_helper(app, client):
    @app.route("/getjson")
    def json_handler(req, resp):
        resp.json = {"name": "goat"}

    response = client.get(url("/getjson"))
    json_body = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "goat"


def test_html_response_helper(app, client):
    @app.route("/html")
    def html_handler(req, resp):
        resp.html = app.template(
            "index.html",
            context={"name": "Goat", "title": "A fast and simple framework"},
        )

    response = client.get(url("/html"))

    assert "text/html" in response.headers["Content-Type"]
    assert "Goat" in response.text
    assert "A fast and simple framework" in response.text


def test_text_response_helper(app, client):
    response_text = "Just Plain Text"

    @app.route("/text")
    def text_handler(req, resp):
        resp.text = response_text

    response = client.get(url("/text"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response_text


def test_manually_setting_body(app, client):
    @app.route("/body")
    def text_handler(req, resp):
        resp.body = b"Byte Body"
        resp.content_type = "text/plain"

    response = client.get(url("/body"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"


def test_status_code(app, client):
    @app.route("/xxx")
    def cool(req, resp):
        resp.text = "not xxx things"
        resp.status_code = 215

    assert client.get(url("/xxx")).status_code == 215


def test_default_404_response(app, client):
    response = client.get("http://testserver/notfound")

    assert response.status_code == 404
    assert response.text == "Sorry, page not Found."


def test_goat_test_client_can_send_request(app, client):
    RESPONSE_TEXT = "THIS IS A MESSAGE FOR YOU"

    @app.route("/hey")
    def cool(req, resp):
        resp.body = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT

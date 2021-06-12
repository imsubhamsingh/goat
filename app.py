from tests.conftest import api
from api import API

app = API()


"""
Creating functions here to test out request
handlers from different routes  using flash way :)
"""


@app.route("/index")
def index(request, response):
    response.text = "Hola from index page"


@app.route("/about")
def about(request, response):
    response.text = "Namaste from about page :)"


# custom parameterized route
@app.route("/who/{name}")
def greet(request, response, name):
    response.text = f"Bonjour, {name}"


@app.route("/age/{age:d}")
def say_your_age(request, response, age):
    response.text = f"Your age is {age}"


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


# class Based handler
@app.route("/pizza")
class PizzaHandler:
    def get(self, request, response):
        print(response)
        response.text = "Order Pizza"

    # def post(self, request, response):
    #     response.text = "Endpoint to queue a pizza"


# django way of adding routes
def handler(request, response):
    response.text = "Django way of routes"


def handler2(request, response):
    response.text = "Django new support"


def json_handler(req, resp):
    resp.json = {"Added by": "alternative method"}


app.add_route("/django", handler)
app.add_route("/hidjango", handler2)
app.add_route("/alternative", json_handler)

# handler for template
@app.route("/template")
def template_handler(request, response):
    response.body = app.template(
        "index.html", context={"name": "Goat", "title": "A fast and simple framework"}
    ).encode()

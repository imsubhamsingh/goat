from tests.conftest import api
from goat.api import API
from middleware import Middleware

app = API()


def custom_exception_handler(request, response, exception_cls):
    response.body = "Oops! Something went wrong. Please, report to Goat Support."


app.add_exception_handler(custom_exception_handler)


@app.route("/error")
def exception_throwing_error(request, response):
    raise AssertionError("This handler should not be used")


"""
Creating functions here to test out request
handlers from different routes  using flash way :)
"""


@app.route("/index")
def index(request, response):
    response.body = "Hola from index page"


@app.route("/about")
def about(request, response):
    response.body = "Namaste from about page :)"


# custom parameterized route
@app.route("/who/{name}")
def greet(request, response, name):
    response.body = f"Bonjour, {name}"


@app.route("/age/{age:d}")
def say_your_age(request, response, age):
    response.body = f"Your age is {age}"


@app.route("/home")
def home(request, response):
    response.body = "Hello from the HOME page"


# class Based handler
@app.route("/pizza")
class PizzaHandler:
    def get(self, request, response):
        print(response)
        response.body = "Order Pizza"

    # def post(self, request, response):
    #     response.text = "Endpoint to queue a pizza"


# django way of adding creating routes
def handler(request, response):
    response.body = "Django way of routes"


def handler2(request, response):
    response.body = "Django new support"


def json_handler(req, resp):
    resp.json = {"This": "IS JSON!!"}


# plug all the url routes here
app.add_route("/django", handler)
app.add_route("/hidjango", handler2)
app.add_route("/give/json", json_handler)

# handler for template
@app.route("/template")
def template_handler(request, response):
    response.body = app.template(
        "index.html", context={"name": "Goat", "title": "A fast and simple framework"}
    ).encode()


# A Simple middleware
class SimpleCustomMiddleware(Middleware):
    def process_request(self, request):
        print(f"Processing request by {self} on {request.url}")

    def process_response(self, request, response):
        print(f"Processing response by {self} on {request.url}")


# plug the middleware to the app
app.add_middleware(SimpleCustomMiddleware)

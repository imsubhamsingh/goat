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

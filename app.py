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

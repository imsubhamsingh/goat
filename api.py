from webob import Request, Response


class API:
    """
    GOAT API
    """

    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            print(self.routes)
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        """
        Entrypoint callable receives three params
        :self
        :param environ
        :param start_response
        """
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def default_response(self, response):
        response.status_code = 404
        response.text = "Sorry, page not Found."

    def handle_request(self, request):
        """
        Method for response creation
        """
        user_agent = request.environ.get("HTTP_USER_AGENT", "NO Agent Found")
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

        # response.text = f"Hello Goat , with this user agent: {user_agent}"
        self.default_response(response)
        return response

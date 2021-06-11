from webob import Request, Response


class API:
    """
    GOAT API
    """

    def __init__(self):
        self.routes = {}

    def route(self, path):
        """
        Add a new route
        """

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
        """
        Returns the default response for page not found
        """
        response.status_code = 404
        response.text = "Sorry, page not Found."

    def find_handler(self, request_path):
        """
        Method to find not only the method that corresponds
        to the path but also the keyword params
        """
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    def handle_request(self, request):
        """
        Method for response creation
        """

        response = Response()

        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

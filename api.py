import inspect
from webob import Request, Response
from parse import parse


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
        assert path not in self.routes, "Such route already exists."

        def wrapper(handler):
            self.routes[path] = handler
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
            result = parse(path, request_path)
            if result is not None:
                return handler, result.named
        return None, None

    def handle_request(self, request):
        """
        Method for response creation
        """

        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

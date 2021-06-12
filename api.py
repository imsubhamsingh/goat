import os
import inspect
from webob import Request, Response
from parse import parse
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader


class API:
    """
    GOAT API
    """

    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

    def route(self, path):
        """
        Decorator that adds a new route, also
        restricts same routes.
        """

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def add_route(self, path, handler):
        """
        An alternate django way to add routes
        """
        assert path not in self.routes, "Such route already exists."

        self.routes[path] = handler

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

    def test_session(self, base_url="http://testserver"):
        """
        Test client
        To use the request WSGI Adapter , we need to mount the
        it to a Session object.
        https://docs.python-requests.org/en/master/user/advanced/
        """
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        """
        handles template's context values
        """
        if context is None:
            context = {}
        return self.templates_env.get_template(template_name).render(**context)

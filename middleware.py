from goat.requests import Request


class Middleware:
    """
    A Base middleware have ability to add another
    middleware that wraps our wsgi app.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """
        As middleware are the first entrypoint to our
        app, so we have implemented wsgi interface.
        """
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        """
        Ability to add another middleware to the
        stack and wrap it around the current app.
        """
        self.app = middleware_cls(self.app)

    def process_request(self, request):
        """
        Method to process the request.
        """
        pass

    def process_response(self, request, response):
        """
        Method to process the reposnse.
        """
        pass

    def handle_request(self, request):
        """
        Method that handles incoming requests
        """
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response

from webob import Request, Response


class API:
    def __call__(self, environ, start_response):
        """
        Entrypoint callable receives three params
        :self
        :param environ
        :param start_response
        """
        request = Request(environ)
        response = Response()
        response.text = "Hello, World, This is Goat"

        return response(environ, start_response)

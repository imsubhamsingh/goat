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

        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        """
        Method for response creation
        """
        user_agent = request.environ.get("HTTP_USER_AGENT", "NO Agent Found")

        response = Response()
        response.text = f"Hello Goat , with this user agent: {user_agent}"

        return response

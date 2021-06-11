class API:
    def __call__(self, environ, start_response):
        """
        Entrypoint callable receives three params
        :self
        :param environ
        :param start_response
        """
        response_body = b"Hello, World"
        status = "200 OK"
        start_response(status, headers=[])
        return iter([response_body])

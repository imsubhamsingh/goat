from http import HTTPStatus


class HTTPError(Exception):
    def __init__(self, status):
        assert isinstance(status, int), "Status should be an integer."
        self._http_status = HTTPStatus(status)

    @property
    def status(self):
        return self._http_status.value

    @property
    def status_phase(self):
        return self._http_status.phrase

    def __str__(self):
        return f"{self.status} {self.status_phase}"

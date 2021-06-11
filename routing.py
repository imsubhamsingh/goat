class Route:
    """
    Class for representing a route to a handler.
    """

    def __init__(self, path, handler):
        self.path = path
        self.handler = handler

class Unauthorized(Exception):
    """
    401 Unauthorized

    Raise if the user is not authorized to access a resource.
    """


class APIConnectionError(Exception):
    pass

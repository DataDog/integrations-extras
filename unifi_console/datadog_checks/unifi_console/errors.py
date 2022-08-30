class CheckConnectionError(Exception):
    """
    Could not connect
    """


class TimeoutError(CheckConnectionError):
    """
    Connection timeout
    """


class Unauthorized(Exception):
    """
    401 Unauthorized

    Raise if the user is not authorized to access a resource.
    """

HTTP_ERRORS = {} # Keys are HTTP status codes, values are Error classes.


def http_error(number):
    def inner(class_):
        HTTP_ERRORS[number] = class_
        class_.status_code = number
        return class_
    return inner


class Error(Exception):
    """Base class for all amber_lib errors."""
    def __init__(self, *args, **kwargs):
        super(Error, self).__init__(*args, **kwargs)


@http_error(400)
class BadRequest(Error):
    pass


@http_error(401)
class Unauthorized(Error):
    pass


@http_error(403)
class Forbidden(Error):
    pass


@http_error(404)
class NotFound(Error):
    pass


@http_error(405)
class MethodNotAllowed(Error):
    pass


@http_error(406)
class NotAcceptable(Error):
    pass


@http_error(410)
class Gone(Error):
    pass


@http_error(415)
class UnsupportedMediaType(Error):
    pass


@http_error(418)
class ImaTeapot(Error):
    pass


@http_error(419)
class AuthenticationTimeout(Error):
    pass


@http_error(500)
class ServerError(Error):
    pass


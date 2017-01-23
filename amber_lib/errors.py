HTTP_ERRORS = {}

def http_error(number):
    def inner(class_):
        HTTP_ERRORS[number] = class_
        class_.status_code = number
        return class_
    return inner


class HTTPError(Exception):
    def __init__(self, *args, **kwargs):

        super(HTTPError, self).__init__(*args, **kwargs)


@http_error(400)
class BadRequest(HTTPError):
    pass


@http_error(401)
class Unauthorized(HTTPError):
    pass


@http_error(403)
class Forbidden(HTTPError):
    pass


@http_error(404)
class NotFound(HTTPError):
    pass


@http_error(405)
class MethodNotAllowed(HTTPError):
    pass


@http_error(406)
class NotAcceptable(HTTPError):
    pass


@http_error(410)
class Gone(HTTPError):
    pass


@http_error(415)
class UnsupportedMediaType(HTTPError):
    pass


@http_error(418)
class ImaTeapot(HTTPError):
    pass


@http_error(419)
class AuthenticationTimeout(HTTPError):
    pass


@http_error(500)
class ServerError(HTTPError):
    pass



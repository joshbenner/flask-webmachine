class Resource(object):
    def __init__(self, request, response):
        """
        :param request: The request
        :type request: flask.Request

        :param response: The response
        :type response: flask.Response
        """
        self.request = request
        self.response = response

    def service_available(self):
        """:rtype: bool"""
        return True

    def known_methods(self):
        """:rtype: tuple[str]"""
        return ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT',
                'OPTIONS')

    def uri_too_long(self):
        """:rtype: bool"""
        return False

    def allowed_methods(self):
        """:rtype: tuple[str]"""
        return 'GET', 'HEAD'

    def malformed_request(self):
        """:rtype: bool"""
        return False

    def is_authorized(self):
        """:rtype: bool or str"""
        return True

    def forbidden(self):
        """:rtype: bool"""
        return False

    def known_content_type(self):
        """:rtype: bool"""
        return True

    def valid_content_headers(self):
        """:rtype: bool"""
        return True

    def valid_entity_length(self):
        """:rtype: bool"""
        return True

    def options(self):
        """
        Pairs of header name and value to respond in OPTIONS request.

        :rtype: list[tuple[str, str]]
        """
        return []

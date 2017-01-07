from six import string_types

from .resource import Resource


class DecisionCore(object):
    def __init__(self, resource_cls, request, response):
        """
        :param resource_cls: The resource being requested.
        :type resource_cls: type

        :param request: The request.
        :type request: flask.Request

        :param response: The response.
        :type response: flask.Response
        """
        self.resource = resource_cls(request, response)  # type: Resource
        self.request = request
        self.response = response
        self.__flow = {
            self.b13: (self.b12, 503),
            self.b12: (self.b11, 501),
            self.b11: (414, self.b10),
            self.b10: (self.b9, 405),
            self.b9: (400, self.b8),
            self.b8: (self.b7, 401),
            self.b7: (403, self.b6),
            self.b6: (501, self.b5),
            self.b5: (415, self.b4),
            self.b4: (413, self.b3),
            self.b3: (200, self.c3)
        }

    def b13(self):
        """Available?"""
        return self.resource.service_available()

    def b12(self):
        """Known method?"""
        return self.request.method in self.resource.known_methods()

    def b11(self):
        """URI too long?"""
        return self.resource.uri_too_long()

    def b10(self):
        """Is method allowed on this resource?"""
        return self.request.method in self.resource.allowed_methods()

    def b9(self):
        """Malformed?"""
        return self.resource.malformed_request()

    def b8(self):
        """Authorized?"""
        auth = self.resource.is_authorized()
        if auth is True:
            return True
        if isinstance(auth, string_types):
            self.response.headers['WWW-Authenticate'] = auth
        return False

    def b7(self):
        """Forbidden?"""
        return self.resource.forbidden()

    def b6(self):
        """Unknown or unsupported Content-* header?"""
        return not self.resource.valid_content_headers()

    def b5(self):
        """Unknown Content-Type?"""
        return not self.resource.known_content_type()

    def b4(self):
        """Request entity too large?"""
        return not self.resource.valid_entity_length()

    def b3(self):
        """OPTIONS?"""
        if self.request.method == 'OPTIONS':
            self.response.headers.extend(self.resource.options())
            return True
        return False

    def c3(self):
        """Accept exists?"""
        return 'http-accept' in self.request.headers

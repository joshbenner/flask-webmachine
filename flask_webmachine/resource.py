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

    def content_types_provided(self):
        """
        :return: Pairs of content-type => handler
        :rtype: list[tuple[str, callable]]
        """
        return []

    def languages_provided(self):
        """
        :return: List of languages this resource is available in, or None to
            skip language negotiation for this resource.
        :rtype: list[str]|None
        """
        return None

    def charsets_provided(self):
        """
        :return: List of charset/converter pairs, or None to skip charset
            negotiation.
        :rtype: list[tuple[str, callable]]|None
        """
        return None

    def encodings_provided(self):
        """
        :return: List of encoding/encoder pairs, or None to skip negotiation.
        :rtype: list[str, callable]|None
        """
        return None

    def resource_exists(self):
        """:rtype: bool"""
        return True

    def previously_existed(self):
        """:rtype: bool"""
        return False

    def moved_permanently(self):
        """
        :return: False or the string URI where it's been moved.
        :rtype: bool|str
        """
        return False

    def moved_temporarily(self):
        """
        :return: False or the string URI where it's been moved.
        :rtype: bool|str
        """
        return False

    def allow_missing_post(self):
        """
        :return: Should POST be allowed to non-existing resource?
        :rtype: bool
        """
        return False

    def is_conflict(self):
        """
        :return: Return True if request represents a conflict.
        :rtype: bool
        """
        return False

    def content_types_accepted(self):
        """
        Handlers for specific content types.

        These handlers will often be responsible for any side-effects a request
        will have, such as creating or updating a resource.

        :return: List of content type/handler pairs.
        :rtype: list[tuple[str, callable]]
        """
        return []

    def generate_etag(self):
        """:rtype: str|None"""
        return None

    def last_modified(self):
        """
        :return: Datetime of last modification (make tz-aware to avoid bugs).
        :rtype: datetime.datetime|None
        """
        return None

    def post_is_create(self):
        """
        :return: Whether POSTing to this resource creates a resource.
        :rtype: bool
        """
        return False

    def created_path(self):
        """
        :return: The path created for a POST to this resource.
        :rtype: str|None
        """
        return None

    def process_post(self):
        """
        Handle POST to this resource.
        """

    def delete_resource(self):
        """
        :return: Whether the resource was deleted.
        :rtype: bool
        """
        return False

    def multiple_choices(self):
        """:rtype: bool"""
        return False

    def expires(self):
        """
        :return: The datetime this resource should be considered stale (use tz-
            aware datetime to avoid bugs).
        :rtype: datetime.datetime|None
        """
        return None

from collections import OrderedDict
import datetime

from six import string_types
import pytz

from .resource import Resource


class InvalidResource(Exception):
    pass


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

    def flow(self):
        return {
            self.b3: (200, self.c3),
            self.b4: (413, self.b3),
            self.b5: (415, self.b4),
            self.b6: (501, self.b5),
            self.b7: (403, self.b6),
            self.b8: (self.b7, 401),
            self.b9: (400, self.b8),
            self.b10: (self.b9, 405),
            self.b11: (414, self.b10),
            self.b12: (self.b11, 501),
            self.b13: (self.b12, 503),
            self.c3: (self.c4, self.d4),
            self.c4: (self.d4, 406),
            self.d4: (self.d5, self.e5),
            self.d5: (self.e5, 406),
            self.e5: (self.e6, self.f6),
            self.e6: (self.f6, 406),
            self.f6: (self.f7, self.g7),
            self.f7: (self.g7, 406),
            self.g7: (self.g8, self.h7),
            self.g8: (self.g9, self.h10),
            self.g9: (self.h10, self.g11),
            self.g11: (self.h10, 412),
            self.h7: (412, self.i7),
            self.h10: (self.h11, self.i12),
            self.h11: (self.h12, self.i12),
            self.h12: (412, self.i12),
            self.i4: (301, self.p3),
            self.i7: (self.i4, self.k7),
            self.i12: (self.i13, self.l13),
            self.i13: (self.j18, self.k13),
            self.k5: (301, self.l5),
            self.k7: (self.k5, self.l7),
            self.k13: (self.j18, self.l13),
            self.l5: (307, self.m5),
            self.l7: (self.m7, 404),
            self.l13: (self.l14, self.m16),
            self.l14: (self.l15, self.m16),
            self.l15: (self.m16, self.l17),
            self.l17: (self.m16, 304),
            self.m5: (self.n5, 410),
            self.m7: (self.n11, 404),
            self.m16: (self.m20, self.n16),
            self.m20: (self.o20, 202),
            self.n5: (self.n11, 410),
            self.n11: (303, self.p11),
            self.n16: (self.n11, self.o16),
            self.o14: (409, self.p11),
            self.o16: (self.o14, self.o18),
            self.o18: (300, 200),
            self.o20: (self.o18, 204),
            self.p3: (409, self.p11),
            self.p11: (201, self.o20)
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

    def c4(self):
        """Acceptable media type available?"""
        provided = OrderedDict(self.resource.content_types_provided())
        best = self.request.accept_mimetypes.best_match(provided.keys())
        if best is None:
            return False
        self.response.content_type = best
        return True

    def d4(self):
        """Accept-Language exists?"""
        return 'accept-language' in self.request.headers

    def d5(self):
        """Acceptable language available?"""
        provided = self.resource.languages_provided()
        if provided is not None:
            best = self.request.accept_languages.best_match(provided)
            if best is None:
                return False
            self.response.content_language = best
        return True

    def e5(self):
        """Accept-Charset exists?"""
        return 'accept-charset' in self.request.headers

    def e6(self):
        """Acceptable charset available?"""
        provided = self.resource.charsets_provided()
        if provided is not None:
            charsets = [c for c, _ in provided]
            best = self.request.accept_charsets.best_match(charsets)
            if best is None:
                return False
            self.response.charset = best
        return True

    def f6(self):
        """Accept-Encoding exists?"""
        return 'accept-encoding' in self.request.headers

    def f7(self):
        """Acceptable encoding available?"""
        provided = self.resource.encodings_provided()
        if provided is not None:
            encodings = [e for e, _ in provided]
            best = self.request.accept_encodings.best_match(encodings)
            if best is None:
                return False
            self.response.content_encoding = best
        return True

    def g7(self):
        """Resource exists?"""
        return self.resource.resource_exists()

    def g8(self):
        """If-Match exists?"""
        return 'if-match' in self.request.headers

    def g9(self):
        """If-Match: * exists?"""
        return self.request.if_match.star_tag

    def g11(self):
        """Etag in If-Match?"""
        return self.resource.generate_etag() in self.request.if_match

    def h7(self):
        """If-Match: * exists?"""
        return self.request.if_match.star_tag

    def h10(self):
        """If-Unmodified-Since exists?"""
        return 'if-unmodified-since' in self.request.headers

    def h11(self):
        """If-Unmodified-Since is valid date?"""
        return self.request.if_unmodified_since is not None

    def h12(self):
        """Last-Modified > If-Unmodified-Since?"""
        last_modified = self.resource.last_modified
        if last_modified is None:
            return False
        return last_modified > self.request.if_unmodified_since

    def i4(self):
        """Server desires that the request be applied to a different URI?"""
        uri = self.resource.moved_permanently()
        if uri is False:
            return False
        self.response.location = uri
        return True

    def i7(self):
        """PUT?"""
        return self.request.method == 'PUT'

    def i12(self):
        """If-None-Match exists?"""
        return 'if-none-match' in self.request.headers

    def i13(self):
        """If-None-Match: * exists?"""
        return self.request.if_none_match.star_tag

    def j18(self):
        """GET/HEAD?"""
        return self.request.method in ('GET', 'HEAD')

    def k5(self):
        """Resource moved permanently?"""
        uri = self.resource.moved_permanently()
        if uri is False:
            return False
        self.response.location = uri
        return True

    def k7(self):
        """Resource previously existed?"""
        return self.resource.previously_existed()

    def k13(self):
        """Etag in If-None-Match?"""
        return self.resource.generate_etag() in self.request.if_none_match

    def l5(self):
        """Resource moved temporarily?"""
        return self.resource.moved_temporarily()

    def l7(self):
        """POST?"""
        return self.request.method == 'POST'

    def l13(self):
        """If-Modified-Since exists?"""
        return 'if-modified-since' in self.request.headers

    def l14(self):
        """If-Modified-Since is valid date?"""
        return self.request.if_modified_since is not None

    def l15(self):
        """If-Modified-Since > Now?"""
        return self.request.if_modified_since > datetime.datetime.now(pytz.UTC)

    def l17(self):
        """Last-Modified > If-Modified-Since?"""
        last_modified = self.resource.last_modified()
        if last_modified is None:
            return False
        return last_modified > self.request.if_modified_since

    def m5(self):
        """POST?"""
        return self.request.method == 'POST'

    def m7(self):
        """Server permits POST to missing resource?"""
        return self.resource.allow_missing_post()

    def m16(self):
        """DELETE?"""
        return self.request.method == 'DELETE'

    def m20(self):
        """Delete enacted? (delete actually happens here)"""
        return self.resource.delete_resource()

    def n5(self):
        """Server permits POST to missing resource?"""
        return self.resource.allow_missing_post()

    def n11(self):
        """Redirect?"""
        self.handle_request_payload()
        if self.resource.post_is_create():
            new_path = self.resource.created_path()
            if new_path is not None:
                self.response.location = new_path
                return True
        else:
            self.resource.process_post()
        return False

    def n16(self):
        """POST?"""
        return self.request.method == 'POST'

    def o14(self):
        """Conflict? (Also: process PUT)"""
        if not self.resource.is_conflict():
            self.handle_request_payload()
            return False
        return True

    def o16(self):
        """PUT?"""
        return self.request.method == 'PUT'

    def o18(self):
        """Multiple representations? (Also: build GET, HEAD body)

        Other methods are routed through here too, but do not have their
        responses built again, since we only do that for GET/HEAD here.
        """
        if self.request.method in ('GET', 'HEAD'):
            self.build_read_response_payload()
        return self.resource.multiple_choices()

    def o20(self):
        """Response includes an entity?"""
        return bool(self.response.data)

    def p3(self):
        """Conflict?"""
        if self.resource.is_conflict():
            return True
        self.handle_request_payload()
        return False

    def p11(self):
        """New resource?"""
        return 'location' in self.response.headers

    def handle_request_payload(self):
        """
        Carry out actions for the request payload (ie: PUT, POST).

        Invokes handlers registered in Resource's content_types_accepted.
        """
        payload_type = self.request.content_type
        acceptable = OrderedDict(self.resource.content_types_accepted())
        if payload_type in acceptable:
            acceptable[payload_type](self.request.data)

    def build_read_response_payload(self):
        """
        Build the response payload for a read request (GET or HEAD).

        Invokes handlers registered in Resource's content_types_provided.
        """
        self.response.set_etag(self.resource.generate_etag())
        self.response.expires = self.resource.expires()
        self.response.last_modified = self.resource.last_modified()
        types_provided = dict(self.resource.content_types_provided())
        renderer = types_provided[self.response.content_type]
        self.response.data = renderer()

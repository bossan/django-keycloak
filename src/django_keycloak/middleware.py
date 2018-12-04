import logging

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from django_keycloak.models import Realm
from django_keycloak.auth import get_remote_user

logger = logging.getLogger(__name__)


def get_realm(request):
    if not hasattr(request, '_cached_realm'):
        request._cached_realm = Realm.objects.first()
    return request._cached_realm


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = get_remote_user(request)
    return request._cached_user


class BaseKeycloakMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        Adds Realm to request.
        :param django.http.request.HttpRequest request: django request
        """
        request.realm = SimpleLazyObject(lambda: get_realm(request))


class RemoteUserAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        Adds user to the request when an authorized user is found in the session
        :param django.http.request.HttpRequest request: django request
        """
        request.user = SimpleLazyObject(lambda: get_user(request))

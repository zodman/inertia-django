from unittest import TestCase
from unittest.mock import MagicMock
from unittest import mock
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import HttpResponse, HttpResponseRedirect
import os

from inertia.share import share


settings.configure(
    VERSION=1, DEBUG=True,
    TEMPLATES= [{
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'APP_DIRS': True,
         'DIRS': [ os.path.join('testutils'), ],
    }],
    INERTIA_SHARE = "test.share_custom_func"
)
django.setup()
from inertia.version import get_version
from inertia.views import render_inertia
from inertia.middleware import InertiaMiddleware


def share_custom_func(request):
    share(request, "custom_data", "custom_value")


class TestInertia(TestCase):
    def test_views(self):
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        self.set_session(request)
        response = render_inertia(request, "Index")
        self.assertTrue(b'id="page"' in response.content)

    def set_session(self, request):
        dict_sessions = {
            'share': {}
        }
        request.session = MagicMock()
        request.session.__getitem__.side_effect = lambda key: dict_sessions[key]

    def test_simple_view(self):
        request = RequestFactory().get("/")
        self.set_session(request)
        response = InertiaMiddleware(lambda x: HttpResponse())(request)
        self.assertTrue(response.status_code==200, response.status_code)

    def test_middlware_missing_header(self):
        view = lambda x: HttpResponse()
        defaults = {
            'X-Inertia': 'true',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Inertia-Version': str(get_version()+1),
        }
        request = RequestFactory().get("/")
        request.headers = defaults
        self.set_session(request)
        response = InertiaMiddleware(view)(request)
        self.assertTrue(response.status_code == 409, response.status_code)

    def test_middleware(self):
        view = lambda request: HttpResponse()
        defaults = {
            'x-Inertia': 'true',
            'X-Inertia-Version': get_version(),
            'x-Requested-With': 'XMLHttpRequest'
        }
        request = RequestFactory().get("/", **defaults)
        request.headers = defaults
        self.set_session(request)
        response = InertiaMiddleware(view)(request)
        self.assertTrue(response.status_code == 200, response.status_code)

    def test_share_custom_data(self):
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        self.set_session(request)
        response = render_inertia(request, "Index")
        self.assertTrue(b'share_custom_data"' in response.content)
        self.assertTrue(b'share_custom_value"' in response.content)

    def test_redirect_303_for_put_patch_delete_requests(self):
        request = RequestFactory().put("/users/1")
        self.set_session(request)
        response = InertiaMiddleware(lambda x: HttpResponseRedirect(redirect_to="/users"))(request)
        self.assertTrue(response.status_code==303, response.status_code)

        request = RequestFactory().patch("/users/1")
        self.set_session(request)
        response = InertiaMiddleware(lambda x: HttpResponseRedirect(redirect_to="/users"))(request)
        self.assertTrue(response.status_code==303, response.status_code)

        request = RequestFactory().delete("/users/1")
        self.set_session(request)
        response = InertiaMiddleware(lambda x: HttpResponseRedirect(redirect_to="/users"))(request)
        self.assertTrue(response.status_code==303, response.status_code)

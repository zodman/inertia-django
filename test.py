from unittest import TestCase
from unittest.mock import MagicMock
from unittest import mock
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import HttpResponse
import os

settings.configure(
    VERSION=1, DEBUG=True,
    TEMPLATES= [{
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'APP_DIRS': True,
         'DIRS': [ os.path.join('testutils'), ],
    }]
)
django.setup()
from inertia.version import asset_version
from inertia.views import render_inertia
from inertia.middleware import InertiaMiddleware

class TestInertia(TestCase):
    def test_views(self):
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        response = render_inertia(request, "Index")
        self.assertTrue(b'id="page"' in response.content)


    def test_middlware_missing_header(self):
        l = lambda request: HttpResponse()
        defaults = {'X-Inertia': True}
        request = RequestFactory().get("/", **defaults)
        dict_sessions = {
            'share': {}
        }
        request.session = MagicMock()
        request.session.__getitem__.side_effect = lambda key: dict_sessions[key]
        response = InertiaMiddleware(l)(request)
        self.assertTrue(response.status_code == 409)

    def test_middleware(self):
        l = lambda request: HttpResponse()
        defaults = {
            'X-Inertia': True,
            'X-Inertia-Version': asset_version.get_version()
        }
        request = RequestFactory().get("/", **defaults)
        dict_sessions = {
            'share': {}
        }
        request.session = MagicMock()
        request.session.__getitem__.side_effect = lambda key: dict_sessions[key]
        response = InertiaMiddleware(l)(request)
        self.assertTrue(response.status_code == 200, response.status_code)

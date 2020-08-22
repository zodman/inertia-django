from unittest import TestCase
from unittest.mock import MagicMock
from unittest import mock
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import HttpResponse

settings.configure(
    VERSION=1, DEBUG=True,
)
django.setup()

from inertia.views import render_inertia
from inertia.middleware import InertiaMiddleware 

class TestInertia(TestCase):
    @mock.patch('inertia.views.render')
    def test_views(self, mock_render):
        mock_render = MagicMock()
        mock_render.return_value = True
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        render_inertia(request, "Index")

    def test_middlware_missing_header(self):
        l = lambda request: HttpResponse()
        request = RequestFactory().get("/")
        dict_sessions = { 
            'share': {}
        }
        request.session = MagicMock()
        request.session.__getitem__.side_effect = lambda key: dict_sessions[key]
        response = InertiaMiddleware(l)(request)
        self.assertTrue(response.status_code == 409)

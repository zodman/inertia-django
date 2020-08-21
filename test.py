from unittest import TestCase
from unittest.mock import MagicMock
import django
from django.conf import settings

settings.configure(
    VERSION=1,DEBUG=True,
)
django.setup()

from inertia.views import render_inertia
from django.test import RequestFactory
from django.http import HttpResponse
from django.contrib.sessions.middleware import SessionMiddleware
from inertia.middleware import InertiaMiddleware 

class TestInertia(TestCase):
    def __test_views(self):
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        render_inertia(request, "Index")

    def test_middlware(self):
        l = lambda request: HttpResponse()
        request = RequestFactory().get("/")
        dict_sessions = { 
            'share': {}
        }
        request.session = MagicMock()
        request.session.__getitem__.side_effect = lambda key: dict_sessions[key]
        response = InertiaMiddleware(l)(request)
        self.assertTrue(response.status_code == 200)

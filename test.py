from unittest import TestCase
import django
from django.conf import settings

settings.configure(
    VERSION=1,DEBUG=True,
                   )
django.setup()

from inertia.views import render_inertia
from django.test import RequestFactory



class TestInertia(TestCase):
    def test_views(self):
        requestfactory = RequestFactory()
        request = requestfactory.get("/")
        render_inertia(request, "Index")

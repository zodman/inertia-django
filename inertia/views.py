import json
from inspect import signature
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.middleware import csrf
from django.urls import get_callable
from .share import share
from .version import get_version

from django.views.generic import View
from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
import logging

log = logging.getLogger(__name__)


def load_lazy_props(d, request):
    for k, v in d.items():
        if isinstance(v, dict):
            load_lazy_props(v, request)
        elif callable(v):
            # evaluate prop and pass request if prop accept it
            if len(signature(v).parameters) > 0:
                d[k] = v(request)
            else:
                d[k] = v()


def _build_context(component_name, props, version, url):
    context = {
        "page": {
            "version": version,
            'url': url,
            "component": component_name,
            "props": props
        },
    }
    return context


def render_inertia(request, component_name, props=None, template_name=None):
    """
    Renders either an HttpRespone or JsonResponse of a component for
    the use in an InertiaJS frontend integration.
    """
    inertia_template = None
    inertia_template = getattr(settings, "INERTIA_TEMPLATE", "base.html")

    if template_name is not None:
        inertia_template = template_name

    if inertia_template is None:
        raise ImproperlyConfigured(
            "No Inertia template found. Either set INERTIA_TEMPLATE"
            "in settings.py or pass template parameter."
        )

    # share custom data or default authenticated user
    share_method_path = getattr(settings, "INERTIA_SHARE", "inertia.share.share_auth")
    if share_method_path:
        share_method = get_callable(share_method_path)
        share_method(request)

    if props is None:
        props = {}
    shared = {}
    if hasattr(request, "session"):
        for k, v in request.session.get("share", {}).items():
            log.debug((k,v))
            shared[k]=v
        props.update(shared)

    for key in ("success", "error", "errors"):
        if hasattr(request, "session") and request.session.get(key):
            del request.session[key]

    # subsequent renders
    inertia_version = get_version()
    is_version_correct = 'X-Inertia-Version' in request.headers and \
                         request.headers["X-Inertia-Version"] == str(inertia_version)

    # check if partial reload is requested
    only_props = request.headers.get("X-Inertia-Partial-Data", [])
    if (
        only_props
        and request.headers.get("X-Inertia-Partial-Component", "") == component_name
    ):
        _props = {}
        for key in props:
            if key in only_props:
                _props.update({key: props[key]})
    else:
        _props = props

    # lazy load props and make request available to props being lazy loaded
    load_lazy_props(_props, request)

    if 'X-Inertia' in request.headers:
        response = JsonResponse({
            "component": component_name,
            "props": _props,
            "version": inertia_version,
            "url": request.get_full_path()
        })
        response['X-Inertia'] = True
        response['Vary'] = 'Accept'
        return response
    context = _build_context(component_name, _props,
                             inertia_version,
                             url=request.get_full_path())
    return render(request, inertia_template, context)

class InertiaMixin:
    component_name = ""
    props = None

    def get_data(self, context):

        return context


    def render_to_response(self, context, **kwargs):
        if self.props is None:
            self.props = {}
        self.props.update(self.get_data(context))
        return render_inertia(self.request, self.component_name, self.props, self.template_name)

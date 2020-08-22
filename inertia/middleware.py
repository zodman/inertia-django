from django.http import HttpResponse
from .share import share
from .version import asset_version


class InertiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        isInertia = request.META.get("X-Inertia")
        assert isInertia, "The client not send X-Inertia Header"
        inertia_version = asset_version.get_version()
        if request.method == "GET" and \
                request.META.get("X-Inertia-Version") != inertia_version:
            request.session.flush()
            response = HttpResponse(status=409)
            response["X-Inertia-Location"] = request.get_full_path_info()
            return response
        share(request, "flash", {
            'success': request.session.get("success", False),
            'error': request.session.get("error", False)
        })
        share(request, 'errors', request.session.get("errors", []))
        response = self.get_response(request)
        return response

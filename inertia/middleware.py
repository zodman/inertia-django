from django.http import HttpResponse
from .share import share
from .version import asset_version


class InertiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            isInertia = request.headers.get("X-Inertia", False)
            assert isInertia, "The client not send X-Inertia Header"
            inertia_version = asset_version.get_version()
            inertia_version_header = str(request.headers.get("X-Inertia-Version", "")) 
            if inertia_version_header != "" and \
                    inertia_version_header != str(inertia_version):
                response = HttpResponse(status=409)
                response["X-Inertia-Location"] = request.get_full_path_info()
                return response
        share(request, "flash", {
            'success': request.session.get("success", False),
            'error': request.session.get("error", False)
        })
        share(request, 'errors', request.session.get("errors", {}))
        response = self.get_response(request)
        return response

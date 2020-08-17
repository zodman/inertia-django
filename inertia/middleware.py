from .share import share

class InertiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        share(request, "flash", {'success': request.session.get("success",False),
                                 'error': request.session.get("error", False)})
        share(request, 'errors', request.session.get("errors",[]) )
        response = self.get_response(request)
        return response

import logging

log = logging.getLogger(__name__)

def share(request, key, value):
    request.session.setdefault("share",{})
    request.session["share"][key]=value

# used in pingcrm ...
def share_flash(request, success=False, error=False, errors=False):
    if success:
        request.session["success"]=success
    if error:
        request.session["error"] = error

    if errors:
        request.session["errors"] = errors

    # log.info(("share", success, error, errors))
    share(request, "flash",{'success':success,'error':error})
    if errors:
        share(request, "errors",errors)


def share_auth(request):
    """Default function for globally sharing authentication data. It can be
    overriden with a custom function defined in SHARE_INERTIA."""
    auth = {}
    if request.user.is_authenticated:
        auth = {
            "id": request.user.id,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }

    share(request, "auth", auth)

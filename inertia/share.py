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
        request.session["error"] = errors

    log.info(("share", success, error, errors))
    share(request, "flash",{'success':success,'error':error})
    if errors:
        share(request, "errors",errors)

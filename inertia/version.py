from django.conf import settings


def get_version():
    asset_version = settings.get("VERSION", 1)
    if callable(asset_version):
        return asset_version()
    else:
        return asset_version

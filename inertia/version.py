from django.conf import settings


def get_version():
    try:
        asset_version = settings.VERSION
    except AttributeError:
        asset_version = 1
    if callable(asset_version):
        return asset_version()
    else:
        return asset_version

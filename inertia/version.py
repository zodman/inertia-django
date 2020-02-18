# pragma pylint: disable=unused-variable
# pragma pylint: disable=not-callable
from django.conf import settings

class Version:

    def set_version(self, version):
        self.asset_version = version
        #print(f"VERSION: {self.asset_version}")

    def get_version(self):
        if callable(self.asset_version):
            #print(f"VERSION: {self.asset_version}")
            return self.asset_version()
        else:
            #print(f"VERSION: {self.asset_version}")
            return self.asset_version


asset_version = Version()
asset_version.set_version(getattr(settings,"VERSIOn",1))

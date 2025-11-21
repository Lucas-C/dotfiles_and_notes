# Script to perform offline validation of a given .readthedocs.yaml configuration file
# cf. https://github.com/readthedocs/readthedocs.org/issues/12561
# INSTALL:
#   sudo apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl
#   git clone --depth 1 git@github.com:readthedocs/readthedocs.org.git && cd readthedocs.org
#   python -m venv . && source bin/activate
#   bin/python -m pip install -r requirements/pip.txt
#   export DJANGO_SETTINGS_MODULE=readthedocs.settings.test
# USAGE: bin/python rtd.py path/to/.readthedocs.yaml
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()  # prevents: AppRegistryNotReady: Apps aren't loaded yet.

from django.conf import settings
from readthedocs.builds.models import APIVersion
from readthedocs.doc_builder.config import load_yaml_config

yml_filepath = Path(sys.argv[1]).absolute().resolve()

settings.DOCROOT = yml_filepath.parent  # prevents: Suspicious operation outside the docroot directory

class DummyProject:
    def checkout_path(self, version=None):
        # prevents: SymlinkOutsideBasePath.SYMLINK_USED / Path traversal via symlink
        return yml_filepath.parent

version = APIVersion()
version.project = DummyProject()
load_yaml_config(version=version, readthedocs_yaml_path=yml_filepath)

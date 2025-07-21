from django.conf import settings
import os
from codeless_django.utils import get_os_file_path
class DocumentationWriter:
    def __init__(self):
        self.file_name=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"

    def write_documentation_url(self):
        os.system(f"cp {get_os_file_path('additional_files/root_urls.py')} {self.file_name}")
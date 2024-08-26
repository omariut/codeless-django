from django.conf import settings
import os

class DocumentationWriter:
    def __init__(self):
        self.file_name=settings_file=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"

    def write_documentation_url(self):
        os.system(f"cp codeless_django/additional_files/root_urls.py {self.file_name}")
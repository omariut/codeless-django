import os
from django.conf import settings
from codeless_django.writers.views import ViewURLWriter
from codeless_django.writers.apis import APIViewURLWriter
from codeless_django.writers.models import ModelWriter
from codeless_django.writers.files import PrepareFiles,AdditionalFileWriter
from codeless_django.writers.base import BaseWriter
from codeless_django.writers.serializers import ModelSerializerWriter
from codeless_django.writers.documentation import DocumentationWriter
from django.conf import settings

class NewAppsWriter(BaseWriter):
    def __init__(self,app_names):
        self.app_names=app_names
        settings_file=settings.ROOT_URLCONF.split(".")[0] + "/settings.py"
        self.file_name=settings_file

    def get_object_header(self):
        return "INSTALLED_APPS+=["

    def get_object_body(self):
        new_apps = "\n"
        for name in self.app_names:
            new_apps+=f"\t \"{name}\", \n"
        return new_apps + "\n]\n"

class IncludeAppUrlToRootUrlWriter(BaseWriter):

    def __init__(self,app_names):
        self.app_names=app_names
        self.file_name=settings.ROOT_URLCONF.split(".")[0] + "/urls.py"
    
    def get_object_header(self):
        return "urlpatterns+=[\n\t"

    def get_include_app_url(self,app_name):
        return f"path('{app_name}/', include('{app_name}.urls')), \n\t"


    def get_object_body(self):
        app_urls=""
        for name in self.app_names:
            app_urls+=self.get_include_app_url(name)
        
        return app_urls + "\n ]\n"





class WriteApps:
    def __init__(self,apps,write_template_views=False,write_api_views=False)-> None:
        self.apps=apps
        self.write_template_views=write_template_views
        self.write_api_views=write_api_views
        self.local_app_names=[app_name for app_name, value in apps.items()]

    def start_app(self,app_name: str) -> None:
        os.system(f"rm -rf {app_name} && python manage.py startapp {app_name}")

    def create_app_folders(self):
        for app_name, value in self.apps.items():
            self.start_app(app_name)

    def initiate_app_urls_and_views_files(self):
        for app_name, value in self.apps.items():
            PrepareFiles(app_name,self.write_api_views)
    
    def write_models(self):
        for app_name, value in self.apps.items():
            models = value["models"]
            for model_name,value in models.items():
                fields=value["fields"]
                meta_options=value["meta_options"]
                ModelWriter(app_name, model_name, fields,meta_options).write_object()
    
    def include_app_urls(self):
        app_names=self.local_app_names
        if self.write_api_views or self.write_template_views:
                IncludeAppUrlToRootUrlWriter(app_names).write_object()

    def include_app_to_settings(self):
        app_names=self.local_app_names.copy()    
        if self.write_api_views:
            app_names.append('rest_framework')
        app_names.append('drf_yasg')

        NewAppsWriter(app_names).write_object()
    
    def write_app_views(self,app_name,model_name):
        if self.write_template_views:
            ViewURLWriter(app_name, model_name).write_views_and_urls()
    
    def write_serializers(self,app_name,model_name):
        if self.write_api_views:
            ModelSerializerWriter(app_name, model_name).write_object()

    def write_app_api_views(self,app_name,model_name):
        if self.write_api_views:
            APIViewURLWriter(app_name, model_name).write_api_views_and_urls()
    
    def write(self):
        file_writer = AdditionalFileWriter()
        file_writer.write_gitignore_file()
        self.create_app_folders()
        self.write_models()
        file_writer.write_new_package_in_requirements_text('drf_yasg', "1.21.5")
        if self.write_api_views:
            file_writer.write_new_package_in_requirements_text('djangorestframework', "3.14.0")
        os.system('pip install -r requirements.txt')
        os.system("python3 manage.py makemigrations")
        os.system("python3 manage.py migrate")
        doc_writer=DocumentationWriter()
        doc_writer.write_documentation_url()
        self.initiate_app_urls_and_views_files()
        self.include_app_to_settings()
        self.include_app_urls()

        
        for app_name, value in self.apps.items():
            models = value["models"]
            for model_name,value in models.items():
                self.write_app_views(app_name, model_name)
                self.write_serializers(app_name, model_name)
                self.write_app_api_views(app_name, model_name)
      
        



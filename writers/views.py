from  codeless_django.writers.base import BaseViewWriter,BaseURLWriter

class CreateViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}CreateView(generic.CreateView):\n"

    def get_object_body(self):
        return f"\tmodel = {self.app_name}_models.{self.model_name}\n\tfields = '__all__'\n\tsuccess_url= ' \ \' "


class ListViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}ListView(generic.ListView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name}\n\tpaginate_by = 10 \n"


class DetailViewWriter(BaseViewWriter):

    def get_object_header(self):
        return f"class {self.model_name}DetailView(generic.DetailView):\n"

    def get_object_body(self):
        return f"\tmodel =  {self.app_name}_models.{self.model_name} \n"

class URLWriter(BaseURLWriter):

    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}/list/', views.{self.model_name}ListView.as_view(), name='{self.model_name.lower()}_list'),\n"
        url_string += f"    path('{self.model_name.lower()}/create/', views.{self.model_name}CreateView.as_view(), name='{self.model_name.lower()}_create'),\n"
        url_string += f"    path('{self.model_name.lower()}/<int:pk>/', views.{self.model_name}DetailView.as_view(), name='{self.model_name.lower()}_detail'),\n"
        return url_string

class ViewURLWriter:

    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.app_name=app_name
    
    def write_views_and_urls(self):
        app_name=self.app_name
        model_name=self.model_name
        ListViewWriter(app_name, model_name).write_object()
        CreateViewWriter(app_name, model_name).write_object()
        DetailViewWriter(app_name, model_name).write_object()
        URLWriter(app_name, model_name).write_object()
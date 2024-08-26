from codeless_django.writers.base import BaseViewWriter,BaseURLWriter


class BaseAPIViewWriter(BaseViewWriter):


    def get_object_body(self):
        return f"\tserializer_class = serializers.{self.model_name}Serializer\n\tqueryset = {self.app_name}_models.{self.model_name}.objects.filter().select_related().prefetch_related()\n\t#authentication_classes=()"


class ListCreateAPIViewWriter(BaseAPIViewWriter):

    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_object_header(self):
        return f"class {self.model_name}ListCreateAPIView(generics.ListCreateAPIView):\n"

class RetrieveUpdateDestroyAPIViewWriter(BaseAPIViewWriter):

    def __init__(self,app_name, model_name):
        super().__init__(app_name,model_name)

    def get_object_header(self):
        return f"class {self.model_name}RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):\n"

class APIUrlWriter(BaseURLWriter):


    def get_url_string(self):
        url_string = ''
        url_string += f"    path('{self.model_name.lower()}s/', views.{self.model_name}ListCreateAPIView.as_view(), name='{self.model_name.lower()}_list_create'),\n"
        url_string += f"    path('{self.model_name.lower()}s/<int:pk>', views.{self.model_name}RetrieveUpdateDestroyAPIView.as_view(), name='{self.model_name.lower()}_retrieve_update_destroy'),\n"
        return url_string




class APIViewURLWriter:

    def __init__(self,app_name, model_name):
        self.model_name = model_name
        self.app_name=app_name
    
    def write_api_views_and_urls(self):
        app_name=self.app_name
        model_name=self.model_name
        ListCreateAPIViewWriter(app_name, model_name).write_object()
        RetrieveUpdateDestroyAPIViewWriter(app_name, model_name).write_object()
        APIUrlWriter(app_name, model_name).write_object()
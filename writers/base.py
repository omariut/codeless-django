from abc import ABC, abstractmethod
class BaseWriter(ABC):
    
    def __init__(self,app_name, model_name,file_name):
        self.model_name = model_name
        self.app_name=app_name
        self.file_name=file_name
    
    @abstractmethod
    def get_object_header(self):
        pass

    @abstractmethod
    def get_object_body(self):
        pass

    def get_object_string(self):
        return self.get_object_header() + self.get_object_body() + '\n'
    
    def write_object(self):
        with open(self.file_name,'a') as f:
            f.write(self.get_object_string()+ "\n\n")


class BaseViewWriter(BaseWriter):

    def __init__(self,app_name, model_name):
        file_name=f"{app_name}/views.py"
        return super().__init__(app_name, model_name,file_name)

    @abstractmethod
    def get_object_header(self):
        pass

    @abstractmethod
    def get_object_body(self):
        pass


class BaseURLWriter(BaseWriter):
    def __init__(self,app_name, model_name,):
        file_name=f"{app_name}/urls.py"
        return super().__init__(app_name, model_name,file_name)


    def get_object_header(self):
        pass


    def get_object_body(self):
        pass
    
    @abstractmethod
    def get_url_string(self):
        pass

    def get_object_string(self):
        url_string=self.get_url_string()
        return "urlpatterns = [\n" + url_string + "]\n"
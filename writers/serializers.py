
import os
from codeless_django.writers.base import BaseWriter

class ModelSerializerWriter(BaseWriter):
    def __init__(self, app_name,model_name):
        file_name=f"{app_name}/serializers.py"

        if not os.path.exists(file_name):
            with open(file_name,'a') as f:
                f.write("from rest_framework import serializers \n \n")
        super().__init__(app_name, model_name, file_name)
    
    def get_object_header(self):
        return f"class {self.model_name}Serializer(serializers.ModelSerializer):\n\n\tclass Meta:\n"
    
    def get_object_body(self):
        return f"\t\tmodel = {self.app_name}_models.{self.model_name}\n\t\tfields = '__all__'"

    

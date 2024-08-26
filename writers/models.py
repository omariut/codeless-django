from codeless_django.writers.base import BaseWriter

class ModelWriter(BaseWriter):

    def __init__(self, app_name, model_name, fields,meta_options):
        self.fields=fields
        self.meta_options=meta_options
        file_name = f"{app_name}/models.py"
        super().__init__(app_name, model_name, file_name)
    
    def get_field_options(self,options):
        return ", ".join([f"{opt['name']}={opt['value']}" for opt in options])
    
    def get_field_string(self,field_name,field_type,options):
        field_options=self.get_field_options(options)
        return f"{field_name} = models.{field_type}({field_options})"

        
    def get_object_header(self):
        return f"class {self.model_name}(models.Model):\n"

    def get_object_body(self):
        model_body="\n"
        for field_name,values in self.fields.items():
           
            field_type=values["type"]
            options=values["options"]
            field_string=self.get_field_string(field_name, field_type, options)
            model_body+= "\t" + field_string + "\n"
        
        if self.meta_options:
            meta_body="\n\tclass Meta: \n"
            for key,value in self.meta_options.items():
                meta_body+=f"\t\t{key}={value}\n"

            return model_body + meta_body
        else:
            return model_body
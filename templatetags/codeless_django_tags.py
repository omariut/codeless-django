from django import template
from codeless_django.data_manager import DataManager

register = template.Library()
data_manager=DataManager(file='codeless_django/fields.json')

@register.filter
def get_options_with_default_values(value):
    fields = data_manager._load_data()
    field_options= fields.get(value,[])
    common_options=fields.get("Common",[])
    return field_options + common_options

@register.filter
def get_all_fields(value):
    fields = data_manager._load_data()
    field_types=list(fields.keys())
    field_types.remove("Common")
    return field_types

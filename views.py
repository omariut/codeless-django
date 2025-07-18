from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import BadRequest
from django.http import HttpResponse
from codeless_django.data_manager import DataManager
from codeless_django.writers.apps import WriteApps
from codeless_django.writers.files import AdditionalFileWriter
from codeless_django.writers.documentation import DocumentationWriter
import os

data_manager=DataManager()
# Create your views here.
@csrf_exempt
def home(request):
    data=data_manager._load_data()
    for option,value in request.POST.items():
        if value:
            print(value)
        
    return render(request, 'codeless_django/demo.html',context=data )

@csrf_exempt
def add_app(request):
    app_name = request.POST.get("app_name")
    data_manager.create_app(app_name.lower())
    return redirect('home')

@csrf_exempt
def add_model(request,app_name):
    model_name = request.POST.get("model_name")
    data_manager.create_model(app_name, model_name)
    return redirect('home')


@csrf_exempt
def add_field(request,model_name,app_name):
    if request.method=="POST":
        request.POST._mutable=True
        field_name =request.POST.pop('field_name')[0]
        field_type = request.POST.pop('field_class')[0]
        data_manager.create_field(app_name, model_name, field_name, field_type)

        for option_name,option_value in request.POST.items():
            if option_value:
                data_manager.create_option(app_name, model_name, field_name, option_name, option_value)
        
        return redirect('home')
    else:
        context={}
        context["field_class"]=request.GET.get('field_class',"")
        context["model_name"]=model_name
        context["app_name"]=app_name
        return render(request, 'codeless_django/forms/field_form.html',context=context)

@csrf_exempt
def add_model_meta(request,model_name,app_name):
    if request.method=="POST":
        for meta_option_name,meta_option_value in request.POST.items():
            if meta_option_value:
                data_manager.create_meta_option(app_name, model_name,meta_option_name, meta_option_value)
        return redirect('home')
    else:
        context={}
        context["model_name"]=model_name
        context["app_name"]=app_name
        return render(request, 'codeless_django/forms/model_meta_form.html',context=context)



def get_field_options(request):
    field_class=request.GET.get('field_class',"")   
    return render(request, 'codeless_django/forms/field_option.html',context={"field_class":field_class}) 

def get_fields(request,model_name,app_name):
    context={}
    context['fields']=data_manager.get_fields(app_name, model_name)
    print(context['fields'])
    return render(request, 'codeless_django/fields.html',context=context)

def delete_app(request,app_name):
    data_manager.delete_app(app_name)
    return redirect('home')

def delete_model(request,app_name,model_name):
    data_manager.delete_model(app_name, model_name)
    return redirect('home')

def delete_field(request,app_name,model_name, field_name):
    data_manager.delete_field(app_name, model_name, field_name)
    return redirect('home')

def delete_meta_options(request,app_name,model_name):
    data_manager.delete_meta_option(app_name, model_name)
    return redirect('home')

@csrf_exempt
def create_apps(request):
    write_template_views=bool(request.POST.get("template_views"))
    write_api_views=bool(request.POST.get("api_views"))
    args = "--api-views" if write_api_views else ""
    args += " --template-views" if write_template_views else ""
    os.system(f"python manage.py writeapps {args}")
    return redirect('/swagger/')

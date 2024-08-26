
from django.urls import path
from codeless_django import views

urlpatterns = [
    path("",views.home,name='home'),
    path('add-app',views.add_app,name='add-app'),
    path('add-model/<str:app_name>',views.add_model,name='add-model'),
    path('field/<str:model_name>/<str:app_name>',views.add_field,name='add-field'),
    path('get_field_options',views.get_field_options,name='get_field_options'),
    path('delete-app/<str:app_name>',views.delete_app, name='delete-app'),
    path('delete-model/<str:app_name>/<str:model_name>',views.delete_model, name='delete-model'),
    path('delete-field/<str:app_name>/<str:model_name>/<str:field_name>',views.delete_field, name='delete-field'),
    path('create-app', views.create_apps, name='create-app'),
    path('add-model-meta/<str:model_name>/<str:app_name>',views.add_model_meta,name='add-model-meta'),
    path('delete-model-meta/<str:model_name>/<str:app_name>',views.delete_meta_options,name='delete-model-meta'),
    path('get-fields/<str:model_name>/<str:app_name>',views.get_fields, name='get-fields' )

]

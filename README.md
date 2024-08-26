# CodeLess-Django

CodeLess-Django is a powerful Django application that enables developers to build Django apps without the need for extensive code writing. By leveraging its intuitive web interface, developers can create apps and models effortlessly. All the essential model field types and options are conveniently presented, allowing developers to make informed decisions easily. With CodeLess-Django, the tedious tasks such as adding apps to the settings file, creating generic views, and API views are handled automatically, streamlining the development process and saving valuable time.

## installation
```
pip install codeless-django
```

## Quick start


1. Add "codeless-django" to your INSTALLED_APPS setting like this::
``` python
    INSTALLED_APPS = [
        ...
        'codeless_django',
    ]
```

2. Include the polls URLconf in your project urls.py like this::
``` python

    path('codeless-django/', include('codeless_django.urls')),
```


3. Start the development server and visit http://127.0.0.1:8000/codeless-django/ to create apps and models.

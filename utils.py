import os

def get_os_file_path(file_path):

    package_name = 'codeless_django'
    package_path = os.path.dirname(__import__(package_name).__file__)
    file_path = os.path.join(package_path, file_path)
    return file_path

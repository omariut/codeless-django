from django.core.management.base import BaseCommand
from codeless_django.writers.apps import WriteApps
from codeless_django.data_manager import DataManager
from django.shortcuts import reverse
data_manager=DataManager()
import os


class Command(BaseCommand):
    help = "Write Models to models.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--template-views",
            action="store_true",
            help="Write template views",
        )
        parser.add_argument(
            "--api-views",
            action="store_true",
            help="Write API views",
        )

    def handle(self, *args, **options):
        write_template_views = options["template_views"]
        write_api_views = options["api_views"]
        data=data_manager._load_data()
        app_writer = WriteApps(data["apps"],write_template_views,write_api_views)
        app_writer.write()
        self.stdout.write("Writing models...")

        documentation_link = " http://127.0.0.1:8000/swagger"
        self.stdout.write(f"Documentation link: {documentation_link}")
        os.system('python manage.py runserver 8000')

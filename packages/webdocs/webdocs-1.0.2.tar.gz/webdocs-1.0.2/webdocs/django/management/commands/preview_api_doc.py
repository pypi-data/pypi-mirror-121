import os
from django.core.management import BaseCommand
from webdocs.preview.flask_app import app


class Command(BaseCommand):
    help = 'preview local openapi doc'

    def add_arguments(self, parser):
        parser.add_argument('--doc_path',
                            help='where the api doc locates',
                            default='../docs/api.yaml')
        parser.add_argument('--host',
                            help='server host',
                            default='127.0.0.1')
        parser.add_argument('--port',
                            help='server port',
                            default=5000)

    def handle(self, *args, **options):
        os.environ.setdefault('API_DOC', options['doc_path'])
        self.stdout.write('you can view editor in /editor ')
        app.run(host=options['host'], port=options['port'])

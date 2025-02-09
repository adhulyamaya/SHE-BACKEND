import os
import subprocess
from django.core.management.commands.runserver import Command as RunserverCommand
import signal

class Command(RunserverCommand):
    def handle(self, *args, **options):
        # Start Celery worker in a subprocess
        celery_worker = subprocess.Popen(
            ['celery', '-A', 'project_companion_backend', 'worker', '--loglevel=info'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Handle Celery worker termination when the server stops
        try:
            super().handle(*args, **options)
        finally:
            # Gracefully terminate Celery when Django server stops
            os.kill(celery_worker.pid, signal.SIGTERM)
            celery_worker.wait()

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# If the DJANGO_SETTINGS_MODULE environment variable is not set,
# use the 'taskmanager.settings' module as the default.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

# Configure Django settings
settings.configure()

# Create Celery application instance
app = Celery('taskmanager')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks
app.autodiscover_tasks()
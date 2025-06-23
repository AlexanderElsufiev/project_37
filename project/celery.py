# СОЗДАНО ПО ОПИСАНИЮ В УРОКЕ 28.2
import os
from celery import Celery

# указание где искать основные настройки
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcdonalds.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# app = Celery('mcdonalds')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



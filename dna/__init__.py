from celery import Celery
from celery.schedules import crontab

from dna.tasks import celery_config
from dna.tasks.external_tasks import show_message

celery = Celery('dna')
celery.config_from_object(celery_config)

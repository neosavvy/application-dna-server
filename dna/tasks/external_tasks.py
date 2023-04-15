from celery import Celery

from dna.tasks import celery_config

celery = Celery('dna')
celery.config_from_object(celery_config)


@celery.task(
    serializer="json",
    name='dna.tasks.external_tasks.show_message'
)
def show_message(message):
    return f"Echo: {message}"

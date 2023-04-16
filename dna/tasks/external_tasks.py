import json

from celery import Celery

from dna.common.data_access.profile_operations import save_or_update_profile
from dna.common.schemas import ProfileUpdate
from dna.tasks import celery_config

celery = Celery('dna')
celery.config_from_object(celery_config)


@celery.task(
    serializer="json",
    name='dna.tasks.external_tasks.show_message'
)
def show_message(message):
    return f"Echo: {message}"


@celery.task(
    serializer="json",
    name='dna.tasks.external_tasks.update_profile_task'
)
def update_profile_task(profile_id, profile):
    print("Async Updating this super fast thing to just prove it can be done")
    profile_update = ProfileUpdate.parse_obj(profile)
    db_profile = save_or_update_profile(profile_update, profile_id)
    print("Should see this update in the UI shortly!")
    return db_profile

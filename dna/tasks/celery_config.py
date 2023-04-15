from kombu import Queue

import dna.config as cfg

print(f"Using user={cfg.RABBITMQ_USER}")
print(f"Using host={cfg.RABBITMQ_HOST}")
print(f"Using scheme={cfg.RABBITMQ_SCHEME}")

broker_url = f'{cfg.RABBITMQ_SCHEME}://{cfg.RABBITMQ_USER}:{cfg.RABBITMQ_PASSWORD}'\
             f'@{cfg.RABBITMQ_HOST}:{cfg.RABBITMQ_PORT}'

worker_concurrency = 4

accept_content = ['json']

task_queues = [
    Queue(name='external'),
    Queue(name='celery')
]

task_routes = {
    'dna.tasks.external_tasks': {'queue': 'external'},
    '*': {'queue': 'celery'},
}


task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'America/New_York'
enable_utc = True

# Debug Only to Synchronously execute delay or apply_async
task_always_eager = False

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

RABBITMQ_PORT = environ.get('RABBITMQ_PORT')
RABBITMQ_HOST = environ.get('RABBITMQ_HOST')
RABBITMQ_USER = environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD')
RABBITMQ_VIRTUAL_HOST = environ.get('RABBITMQ_VIRTUAL_HOST')
RABBITMQ_SCHEME = environ.get('RABBITMQ_SCHEME')

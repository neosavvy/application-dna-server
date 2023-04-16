import os

# check for db environment overrides, and if none found then default to development environment configuration
port = 5432
host = 'db'
user = 'postgres'
password = 'your-super-secret-and-long-postgres-password'
database = 'postgres'

if 'POSTGRES_PORT' in os.environ:
    port = int(os.environ['POSTGRES_PORT'])
if 'POSTGRES_HOST' in os.environ:
    host = os.environ['POSTGRES_HOST']
if 'POSTGRES_USERNAME' in os.environ:
    user = os.environ['POSTGRES_USERNAME']
if 'POSTGRES_PASSWORD' in os.environ:
    password = os.environ['POSTGRES_PASSWORD']
if 'POSTGRES_DB' in os.environ:
    database = os.environ['POSTGRES_DB']
# #########################################################################################################
# SQL Alchemy Setup
# #########################################################################################################

connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(user,
                                                         password,
                                                         host,
                                                         port,
                                                         database)

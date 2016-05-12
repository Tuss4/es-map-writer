import os
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgres://postgres:postgres@{}:5432/postgres'.format(os.getenv('DB_1_PORT_5432_TCP_ADDR')))
assert DATABASE_URL

TYPE_MAP = {  # Maps PostgreSQL data type keys to Elasticsearch data type vals
    'serial primary key': 'integer',
    'integer': 'integer',
    'character varying': 'string',
    'text': 'string',
    'integer': 'integer',
    'timestamp with time zone': 'date',
    'timestamp': 'date',
    'date': 'date',
    'boolean': 'boolean',
    'bytea': 'binary',
    'jsonb': 'object',
    'json': 'object'
}


MAPPING_TEMPLATE = """%(map_name)s_mapping = {
    "mappings": {
        "%(doc_type)s": {
            "properties": %(fields)s
        }
    }
}
"""


def db_conn():
    parts = urlparse(DATABASE_URL)
    db = parts.path.strip('/')
    user = parts.username
    pw = parts.password
    port = parts.port
    host = parts.hostname
    connection = psycopg2.connect(
        host=host, port=port, user=user, password=pw, database=db)
    connection.set_session(autocommit=True)
    return connection

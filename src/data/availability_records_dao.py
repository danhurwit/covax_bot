from datetime import datetime

from decouple import config

from data.query_executor import execute

DB_URL = config('DB_URL')


def create_availability_record(source, site_name):
    publish_datetime = datetime.now().timestamp()
    query = 'INSERT INTO availability_records (source, site_name, publish_datetime) ' \
            'VALUES (?, ?, ?) '
    execute(DB_URL, query, (source, site_name, publish_datetime))

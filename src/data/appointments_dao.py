from datetime import datetime
from typing import List

from decouple import config

from data.query_executor import execute, execute_single_result

DB_URL = config('DB_URL')


def update_site_availability(source: str, site_name: str, availability_date: datetime, num_available: int):
    availability_date = __get_formatted_availability(availability_date)
    query = 'INSERT INTO appointments (source, site_name, availability_date, num_available) ' \
            'VALUES (?, ?, ?, ?) ' \
            'ON CONFLICT(source, site_name, availability_date) DO UPDATE SET num_available = ?'
    execute(DB_URL, query, (source, site_name, availability_date, num_available, num_available))


def reset_availability_excluding(source: str, site_names: List[str]):
    query = 'UPDATE appointments SET ' \
            'num_available = 0 ' \
            'WHERE source = ? ' \
            'AND appointments.site_name NOT IN ({seq})' \
        .format(seq=','.join(['?'] * len(site_names)))
    execute(DB_URL, query, (source,) + tuple(site_names))


def get_site_availability(source: str, site_name: str, availability_date: datetime) -> int:
    availability_date = __get_formatted_availability(availability_date)
    query = 'SELECT num_available FROM appointments ' \
            'WHERE source = ? AND site_name = ? AND availability_date = ?'
    result = execute_single_result(DB_URL, query, (source, site_name, availability_date))
    return int(result[0]) if result else 0


def __get_formatted_availability(availability_date) -> str:
    return availability_date.strftime("%Y-%m-%d")

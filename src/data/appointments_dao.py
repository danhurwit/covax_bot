import sqlite3
from datetime import datetime
from typing import List

from decouple import config

DB_URL = config('DB_URL')


def update_site_availability(source: str, site_name: str, availability_date: datetime, num_available: int):
    availability_date = __get_formatted_availability(availability_date)
    query = 'INSERT INTO appointments (source, site_name, availability_date, num_available) ' \
            'VALUES (?, ?, ?, ?) ' \
            'ON CONFLICT(source, site_name, availability_date) DO UPDATE SET num_available = ?'
    __execute(query, (source, site_name, availability_date, num_available, num_available))


def reset_availability(source: str, site_names: List[str]):
    query = 'UPDATE appointments SET ' \
            'num_available = 0 ' \
            'WHERE source = ? ' \
            'AND appointments.site_name IN ({seq})' \
        .format(seq=','.join(['?'] * len(site_names)))
    __execute(query, (source,) + tuple(site_names))


def get_site_availability(source: str, site_name: str, availability_date: datetime) -> int:
    availability_date = __get_formatted_availability(availability_date)
    query = 'SELECT num_available FROM appointments ' \
            'WHERE source = ? AND site_name = ? AND availability_date = ?'
    result = __execute_single_result(query, (source, site_name, availability_date))
    return int(result[0]) if result else 0


def __get_formatted_availability(availability_date) -> str:
    return availability_date.strftime("%Y-%m-%d")


def __execute_with_results(query: str, values):
    con = sqlite3.connect(DB_URL)
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    con.commit()
    con.close()
    return results


def __execute_single_result(query: str, values):
    con = sqlite3.connect(DB_URL)
    cur = con.cursor()
    cur.execute(query, values)
    result = cur.fetchone()
    con.commit()
    con.close()
    return result


def __execute(query: str, values):
    con = sqlite3.connect(DB_URL)
    cur = con.cursor()
    cur.execute(query, values)
    con.commit()
    con.close()

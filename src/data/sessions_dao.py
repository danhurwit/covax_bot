from datetime import datetime

from decouple import config

from data.query_executor import execute, execute_single_result
from models.sources.SessionState import SessionState

DB_URL = config('DB_URL')


def create_session(source: str, session_id: str, queue_status: SessionState, cookies: str):
    created_at = __get_formatted_availability(datetime.now())
    query = 'INSERT INTO sessions (source, id, created_at, updated_at, queue_status, cookies) ' \
            'VALUES (?, ?, ?, ?, ?, ?) '
    execute(DB_URL, query, (source, session_id, created_at, created_at, queue_status.value, cookies))


def update_queue_status(source: str, session_id: str, queue_status: SessionState):
    updated_at = __get_formatted_availability(datetime.now())
    query = 'UPDATE sessions SET ' \
            'queue_status = ?, ' \
            'updated_at = ?' \
            'WHERE source = ? ' \
            'AND id = ?'
    execute(DB_URL, query, (queue_status.value, updated_at, source, session_id))


def insert_cookies(source: str, session_id: str, cookies: str):
    updated_at = __get_formatted_availability(datetime.now())
    query = 'UPDATE sessions SET ' \
            'cookies = ?, ' \
            'updated_at = ?' \
            'WHERE source = ? ' \
            'AND id = ?'
    execute(DB_URL, query, (cookies, updated_at, source, session_id))


def get_current_session(source: str):
    query = 'SELECT * FROM sessions ' \
            'WHERE source = ? ' \
            'AND (queue_status = ? or queue_status = ?)'
    return execute_single_result(DB_URL, query, (source, SessionState.ENQUEUED.value, SessionState.ACCEPTED.value))


def __get_max_created_at(source: str):
    query = 'SELECT max(created_at) FROM sessions ' \
            'WHERE source = ? '
    return execute_single_result(DB_URL, query, source)


def __get_formatted_availability(created_at):
    return created_at.timestamp()

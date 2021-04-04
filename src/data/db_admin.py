import sqlite3

DB_NAME = 'appointments.db'


def create_appointments_table():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''CREATE TABLE appointments(
                        source text NOT NULL,
                        site_name text NOT NULL, 
                        availability_date text NOT NULL, 
                        num_available real, 
                        PRIMARY KEY(source, site_name, availability_date))''')
    con.commit()
    con.close()


def create_availability_records_table():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''CREATE TABLE availability_records(
                            source text NOT NULL,
                            site_name text NOT NULL, 
                            publish_datetime real NOT NULL, 
                            PRIMARY KEY(source, site_name, publish_datetime))''')
    con.commit()
    con.close()


def create_session_table():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''CREATE TABLE sessions(
                            source text NOT NULL, 
                            id text NOT NULL,
                            created_at real NOT NULL,
                            updated_at real NOT NULL,
                            queue_status text, 
                            cookies text, 
                            PRIMARY KEY(source, created_at))''')
    con.commit()
    con.close()


def create_appointments_indices():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''create index appointments_num_available_index on appointments (num_available)''')
    con.commit()
    con.close()


def create_sessions_indices():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''create index sessions_id on sessions (id)''')
    cur.execute('''create index sessions_created_at on sessions (created_at)''')
    con.commit()
    con.close()


if __name__ == "__main__":
    try:
        create_appointments_table()
    except sqlite3.OperationalError as e:
        print(e)
    try:
        create_session_table()
    except sqlite3.OperationalError as e:
        print(e)
    try:
        create_availability_records_table()
    except sqlite3.OperationalError as e:
        print(e)
    try:
        create_appointments_indices()
    except sqlite3.OperationalError as e:
        print(e)
    try:
        create_sessions_indices()
    except sqlite3.OperationalError as e:
        print(e)

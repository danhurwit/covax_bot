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


def create_indexes():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''create index appointments_num_available_index on appointments (num_available)''')
    con.commit()
    con.close()


if __name__ == "__main__":
    create_appointments_table()
    create_indexes()

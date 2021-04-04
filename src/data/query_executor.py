import sqlite3


def execute_with_results(db_url: str, query: str, values):
    con = sqlite3.connect(db_url)
    con.row_factory = __dict_factory
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    con.commit()
    con.close()
    return results


def execute_single_result(db_url: str, query: str, values):
    con = sqlite3.connect(db_url)
    con.row_factory = __dict_factory
    cur = con.cursor()
    cur.execute(query, values)
    result = cur.fetchone()
    con.commit()
    con.close()
    return result


def execute(db_url: str, query: str, values):
    con = sqlite3.connect(db_url)
    con.row_factory = __dict_factory
    cur = con.cursor()
    cur.execute(query, values)
    con.commit()
    con.close()


def __dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

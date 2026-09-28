import sqlite3

DB = "shop.db"


def query(sql, *args):
    with sqlite3.connect(DB) as conn:
        return [dict(zip([c[0] for c in cur.description], row))
                for cur in [conn.execute(sql, args)] for row in cur]

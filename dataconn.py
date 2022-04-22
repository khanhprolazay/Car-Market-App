import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def select_all_table(db_file, table):
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)
    rows = cur.fetchall()
    return rows
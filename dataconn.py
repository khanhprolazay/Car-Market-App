import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def Filter_hang_xe(conn, query, hang_xe):
    cur = conn.cursor()
    cur.execute(query,[hang_xe])
    rows = cur.fetchall()
    return rows

def executeSelectQuery(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def executeSelectQueryOneContion(conn, query, var):
    cur = conn.cursor()
    cur.execute(query %var)
    rows = cur.fetchall()
    return rows

def executeInsertDeleteQuery(conn, query, values):
    cur = conn.cursor()
    try:
        cur.execute(query, values)
        conn.commit()
        rows = cur.fetchall()
        return rows
    except:
        pass

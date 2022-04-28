import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def Filter_hang_xe(db_file, hang_xe):
    conn = create_connection(db_file)
    cur = conn.cursor()
    query = """
        SELECT id
        FROM Car_data
        WHERE instr(Tieu_de, ?) > 0
        LIMIT 20 OFFSET 20;
    """
    cur.execute(query,[hang_xe])
    rows = cur.fetchall()
    return rows

def executeQuery(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def executeQueryOneContion(conn, query, var):
    cur = conn.cursor()
    cur.execute(query %var)
    rows = cur.fetchall()
    return rows
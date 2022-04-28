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

def select_20_item_from_table(conn, table, begin):
    cur = conn.cursor()
    query = "SELECT * FROM " + table + " LIMIT 20 OFFSET " + str(begin)
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def select_item_id_from_car(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Car_data WHERE id = '%d'" %id)
    rows = cur.fetchall()
    return rows

def select_item_from_like(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Car_data WHERE id in (SELECT car_id FROM Like where username = '%s')" %username)
    rows = cur.fetchall()
    return rows

def select_username(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT Name FROM Login WHERE email = '%s'" %email)
    rows = cur.fetchall()
    return rows[0][0]

def select_item_from_history(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Car_data WHERE id in (SELECT car_id FROM History where username = '%s')" %username)
    rows = cur.fetchall()
    return rows

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
import sqlite3 as sql

DATABASE = 'scripts.sqlite'

def CREATE_TABLE(script):
    conn = sql.connect(DATABASE)
    cur = conn.cursor()
    CREATE_TABLE_SQL = f'''CREATE TABLE IF NOT EXISTS {script}(
        Date TEXT,
        Buy_Price REAL,
        Sell_Price REAL,
        Lot_Size REAL,
        Broker_per REAL,
        Turn_Over REAL,
        Broker_amt REAL,
        Stt REAL,
        Sebi_charges REAL,
        Stamp_Duty REAL,
        Transaction_charges REAL,
        Gst REAL,
        Total_Tax REAL,
        Profit REAL,
        Net_Profit REAL
    );'''
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()



def save_data(script, date, data):
    CREATE_TABLE(script)
    conn = sql.connect(DATABASE)
    cur = conn.cursor()    
    SQL = f'''INSERT INTO {script} VALUES ("{date}", ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cur.execute(SQL, data)
    conn.commit()
    cur.close()
    conn.close()

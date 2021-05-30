import sqlite3


def connect():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    return conn

def resetDB():
    with connect() as db:
        db.execute("DROP TABLE IF EXISTS User")
        db.execute("""
                   CREATE TABLE User (
                     id TEXT PRIMARY KEY,
                     password TEXT,
                     money REAL
                   )
        """)        

    with connect() as db:
        db.execute("DROP TABLE IF EXISTS Stock")
        db.execute("""
                   CREATE TABLE Stock (
                     id INTEGER PRIMARY KEY,
                     ticker TEXT,
                     price REAL,
                     amount INTEGER,
                     uid TEXT,
                     FOREIGN KEY(uid) REFERENCES User(id)
                   )
        """)
    
    with connect() as db:
        db.execute("DROP TABLE IF EXISTS Price")
        db.execute("""
                   CREATE TABLE Price (
                     id TEXT PRIMARY KEY,
                     price REAL,
                     date INTEGER
                   )
        """)

if __name__ == "__main__":
    print("Resetting database")
    resetDB()

        

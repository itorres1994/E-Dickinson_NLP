# Add files to a db
import sqlite3

conn = sqlite3.connect('./e-dickinson.db')

with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE Dickinson(file_name TEXT, poem TEXT)")


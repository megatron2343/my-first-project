import sqlite3
import os

con = sqlite3.connect("photobase.db")
con.close()
con1 = sqlite3.connect("photobase1.db")
con1.close()
os.remove("photobase.db")
os.remove("photobase1.db")
con = sqlite3.connect("photobase.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS first(
   fname TEXT,
   number INT,
   aname TEXT);
""")
con.commit()
cur.execute("INSERT INTO first(fname,number,aname) VALUES (?,?,?)", ('supersecrettest', 1, 'megasecret'))
con.commit()
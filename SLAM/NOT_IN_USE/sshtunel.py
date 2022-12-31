
from sshtunnel import SSHTunnelForwarder
import time

with SSHTunnelForwarder(
         ('pluton.kt.agh.edu.pl', 22),
         ssh_password="password",
         ssh_username="aburban",
         remote_bind_address=('127.0.0.1', 5432)) as server:

    conn = psycopg2.connect(database="dotest",port=server.local_bind_port)
    curs = conn.cursor()
    sql = "select * from node"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)
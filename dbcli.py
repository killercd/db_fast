import argparse
import mysql.connector


parser = argparse.ArgumentParser(description='db client')
parser.add_argument('-s','--host', action="store", dest="host", default="localhost")
parser.add_argument('-u','--user', action="store", dest="user", default="")
parser.add_argument('-p','--password', action="store", dest="password", default="")
parser.add_argument('-d','--database', action="store", dest="database", default="")
parser.add_argument('--tables', action="store_true", dest="show_tables", default="")

parse = parser.parse_args()

conn = mysql.connector.connect(
            host=parse.host,
            user=parse.user,
            password=parse.password,
            database=parse.database
        )

if parse.show_tables:
    

    mycursor = conn.cursor()
    mycursor.execute("SELECT table_name FROM information_schema.tables")
    myresult = mycursor.fetchall()
    for table in myresult:
        print(table[0])



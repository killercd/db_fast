import argparse
import mysql.connector


parser = argparse.ArgumentParser(description='db client')
parser.add_argument('-s','--host', action="store", dest="host", default="localhost")
parser.add_argument('-u','--user', action="store", dest="user", default="")
parser.add_argument('-p','--password', action="store", dest="password", default="")
parser.add_argument('-d','--database', action="store", dest="database", default="")
parser.add_argument('-t','--type', action="store", dest="db_type", default="mysql", help="mysql, postgres")
parser.add_argument('--table', action="store", dest="table_list", default="", help="tbl_user, tbl_address...")

#parser.add_argument('--tables', action="store_true", dest="show_tables", default="")
conn = None
parse = parser.parse_args()
if parse.db_type == "mysql":
    conn = mysql.connector.connect(
                host=parse.host,
                user=parse.user,
                password=parse.password,
                database=parse.database
            )


    

mycursor = conn.cursor()
mycursor.execute("SELECT table_name FROM information_schema.tables")
myresult = mycursor.fetchall()
for table in myresult:
    print(table[0])



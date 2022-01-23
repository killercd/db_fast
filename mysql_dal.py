import mysql.connector
import pdb
class MysqlDal():
    def __init__(self,host, user, password, port=3306, database=""):

        self.host = host
        self.user=user
        self.password=password
        self.port=port
        self.database=database

        self.connection = None
    def connect(self):

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def query(self, query):
        mycursor = self.connection.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult

    def tables(self):
        lst = []
        for tables_t in self.query("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema='{}';".format(self.database)):
            lst.append(tables_t[0])
        return lst
    def add_column(self,name,column,option):
        return self.execute("ALTER TABLE {} ADD({} {})".format(name, column, option))
    def describe(self, table):
        return self.query("DESCRIBE {}".format(table))
    def type_list(self):
        return ['INTEGER','SMALLINT','DECIMAL','NUMERIC','REAL','DOUBLE','DATE','TIME','DATETIME','TIMESTAMP','YEAR','CHAR','VARCHAR','BINARY','VARBINARY','BLOB']


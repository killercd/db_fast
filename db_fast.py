import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *


from PyQt5.QtCore import QSize
from mysql_dal import MysqlDal




class DDLDebugWindow(QMainWindow):

    def print_row(self):
        a = self.structure.currentIndex
        print(a)
    def describe(self):
        


        self.structure = QTableWidget(self)

        self.structure.setColumnCount(6)
        self.structure.setRowCount(5)
        self.structure.setMinimumWidth(500)
        self.structure.setMinimumHeight(500)

        self.structure.setHorizontalHeaderLabels(['Name', 'Type', 'Null', 'Key','Default','Extra'])

        #self.table_list.currentItem()
        #newitem = QTableWidgetItem(item)
        row_num = 0
        cel_num = 0
        for row in self.db_connection.describe(self.table_list.currentItem().text()):
            for cell in list(row):
                try:
                    newitem = QTableWidgetItem(str(cell, "utf-8"))
                except:
                    newitem = QTableWidgetItem(cell)
                self.structure.setItem(row_num, cel_num, newitem)
                cel_num = cel_num+1

            cel_num = 0
            row_num = row_num+1
        
        self.structure.setRowCount(row_num+1)
        self.structure.resize(QSize(420,350))
        self.structure.move(320,10)
        self.structure.itemSelectionChanged.connect(self.print_row)


        self.structure.show()

    def __init__(self, parent=None, db_connection=None):
        
        super(DDLDebugWindow, self).__init__(parent)
        self.db_connection = db_connection
        self.setFixedSize(QSize(900, 600))    
        self.setWindowTitle("Describe Table")
        
        self.table_list = QListWidget(self)
        self.table_list.resize(QSize(300,300))
        self.table_list.move(10,10)
        

        self.btn_describe = QPushButton(self)
        self.btn_describe.move(200,310)
        self.btn_describe.setText("Describe")
        self.btn_describe.clicked.connect(self.describe)

        t_tables = self.db_connection.tables()
        c = 0
        for table in t_tables:
            self.table_list.insertItem(c, table)
            c = c+1

        
        

        


class ExampleWindow(QMainWindow):
    
    def connect(self):
        print("Host: {}".format(self.txt_host.text()))
        self.db_connection = MysqlDal(self.txt_host.text(), self.txt_user.text(), self.txt_password.text(),database=self.txt_database.text())
        self.db_connection.connect()
        tables = self.db_connection.tables()

        self.b.setPlainText("\n".join(tables))
    def draw_row1(self):

        self.lbl_host = QLabel(self)
        self.lbl_host.setText("Host/Ip")
        self.lbl_host.move(10,20)

        self.txt_host = QLineEdit(self)
        self.txt_host.resize(QSize(120,30))
        self.txt_host.move(10,45)
        self.txt_host.setText("localhost")

        self.lbl_port = QLabel(self)
        self.lbl_port.setText("port")
        self.lbl_port.move(160,20)


        self.txt_port = QLineEdit(self)
        self.txt_port.resize(QSize(60,30))
        self.txt_port.move(160,45)

        self.btn_connect = QPushButton(self)
        self.btn_connect.move(300,45)
        self.btn_connect.setText("Connect")
        self.btn_connect.clicked.connect(self.connect)

    def draw_row2(self):
        self.lbl_user = QLabel(self)
        self.lbl_user.resize(QSize(120,50))
        self.lbl_user.setText("User")
        self.lbl_user.move(10,70)
        

        self.txt_user = QLineEdit(self)
        self.txt_user.resize(QSize(120,30))
        self.txt_user.move(10,105)
        self.txt_user.setText("root")

        
        self.lbl_password = QLabel(self)
        self.lbl_password.setText("password")
        self.lbl_password.move(160,80)
        


        self.txt_password = QLineEdit(self)
        self.txt_password.resize(QSize(120,30))
        self.txt_password.move(160,105)
        self.txt_password.setText("5l00g0v5")

        self.lbl_database = QLabel(self)
        self.lbl_database.setText("database")
        self.lbl_database.move(300,80)
        

        self.txt_database = QLineEdit(self)
        self.txt_database.resize(QSize(120,30))
        self.txt_database.move(300,105)
        self.txt_database.setText("droidgen")


    def processtrigger(self, q):
        if (q.text().lower()=="describe"):
            print(q.text()+" is clicked")
            nwin = DDLDebugWindow(self, self.db_connection)
            nwin.show()


    def draw_menu(self):
        self.menu = self.menuBar()
        self.task = self.menu.addMenu("Tables")
        
        self.ddl_debug = QAction("Describe",self)
        self.task.addAction(self.ddl_debug)
        self.task.triggered[QAction].connect(self.processtrigger)

        #self.task.addAction("New")
    def create_gui(self):
        
        self.draw_row1()
        self.draw_row2()
        self.draw_menu()

        # Add text field
        self.b = QPlainTextEdit(self)
        self.b.move(10,140)
        self.b.resize(400,200)

    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(600, 600))    
        self.setWindowTitle("DB Fast") 

        self.create_gui()
        self.db_connection = None
        self.menu = None
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )
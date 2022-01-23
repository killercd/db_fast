from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)

import sys
import mysql.connector

class DescribeObj():
    def __init__(self, column_name, data_type,is_nullable, column_type, column_key,extra):
        self.column_name = column_name 
        self.data_type = data_type 
        self.is_nullable = is_nullable 
        self.column_type = column_type
        self.column_key = column_key
        self.extra = extra

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4
    host = "localhost"
    user = "root"
    password = "5l00g0v5"
    database = "droidgen"
    table_name = None
    def __init__(self):
        super(Dialog, self).__init__()

        self.table_name = sys.argv[1]
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Form Layout - pythonspot.com")
    def connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
    def describe(self):
        ret_lst = []
        conn = self.connection()
        mycursor = conn.cursor()
        mycursor.execute("SELECT COLUMN_NAME, DATA_TYPE,IS_NULLABLE,COLUMN_TYPE,COLUMN_KEY,EXTRA FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(self.database, self.table_name))
        myresult = mycursor.fetchall()
        for obj in myresult:
            ret_lst.append(DescribeObj(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5]))
        return ret_lst
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        # layout.addRow(QLabel("Name:"), QLineEdit())
        # layout.addRow(QLabel("Country:"), QComboBox())
        # layout.addRow(QLabel("Age:"), QSpinBox())
        

        for obj in self.describe():
            type_list = QComboBox()
            type_list.addItems(['INTEGER',
                                'SMALLINT', 
                                'DECIMAL', 
                                'NUMERIC',
                                'FLOAT',
                                'DATE',
                                'DATETIME',
                                'TIME',
                                'YEAR',
                                'CHAR',
                                'VARCHAR',
                                'BLOB',
                                'TEXT'
                                
                                ])
            for i in range(0,type_list.count()):
                if type_list.itemText(i).lower() == obj.data_type.lower():
                    type_list.setCurrentIndex(i)
                    print("{}")
            layout.addRow(QLabel("{}".format(obj.column_name)), type_list)
        self.formGroupBox.setLayout(layout)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
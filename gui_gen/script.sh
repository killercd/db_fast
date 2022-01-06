USER='root'
HOST='localhost'
DB='droidgen'
PASS='5l00g0v5'

for table in $(mysql -u $USER -h $HOST --password=$PASS --database=$DB << EOF 
SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema='$DB';
EOF
)
do
    if [[ $table != "TABLE_NAME" ]]; then
        cat << ESCRIPT > "G_$table.py"
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)

import sys

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("DB $table")
        
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
ESCRIPT

    for column in $(mysql -u $USER -h $HOST -p --database=$DB --password=$PASS -e "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '$DB' AND TABLE_NAME = '$table';" |
            sed '1d')
        do
cat << ESCRIPT >> "G_$table.py"
        
        self.lbl_$column = QLabel(self)
        self.lbl_$column.setText("$column")

        self.txt_$column = QLineEdit(self)
        layout.addRow(self.lbl_$column, self.txt_$column)

ESCRIPT
        done
    fi
cat << ESCRIPT >> "G_$table.py"
        self.formGroupBox.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())

ESCRIPT
done


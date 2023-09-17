from collections import deque
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
        
class DemandQueue(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.history = deque()
        try:
            with open('history.json', "r") as h:
                self.history = deque(json.loads(h.read()))
        except FileNotFoundError:
            with open('history.json', "x") as h:
                h.write("[]")
        except:
            print('File corrupted, recreating? Y/N')
            prompt = input()
            if (prompt == 'y' or prompt == 'Y'):
                with open('history.json', "w") as h:
                    h.write("[]")
            else:
                return
            
        self.table = self.construct_table(self.history)
        
        # Constraint on self.insert_place
        self.onlyInt = QIntValidator(self)
        self.onlyInt.setRange(0, self.table.rowCount())
        
        edit = QWidget(self)
        edit_layout = QHBoxLayout()
        
        name_comp = QWidget(edit)
        name_layout = QVBoxLayout()
        name4name = QLabel("老板名称", name_comp)
        self.name = QTextEdit(name_comp)
        name_layout.addWidget(name4name)
        name_layout.addWidget(self.name)
        name_comp.setLayout(name_layout)
        
        desc_comp = QWidget(edit)
        desc_layout = QVBoxLayout()
        name4desc = QLabel("点播内容", desc_comp)
        self.desc = QTextEdit(desc_comp)
        desc_layout.addWidget(name4desc)
        desc_layout.addWidget(self.desc)
        desc_comp.setLayout(desc_layout)
        
        date_comp = QWidget(edit)
        date_layout = QVBoxLayout()
        name4date = QLabel("点播时间", date_comp)
        self.date = QTextEdit(date_comp)
        date_layout.addWidget(name4date)
        date_layout.addWidget(self.date)
        date_comp.setLayout(date_layout)
        
        edit_layout.addWidget(name_comp)
        edit_layout.addWidget(desc_comp)
        edit_layout.addWidget(date_comp)
        edit.setLayout(edit_layout)
        
        insert = QWidget(self)
        insert_layout = QHBoxLayout()
        append = QPushButton(insert)
        append.setText("添加点播")
        append.clicked.connect(self.append_queue)
        push = QPushButton(insert)
        push.setText("插播")
        push.clicked.connect(self.push_queue)
        pop = QPushButton(insert)
        pop.setText("完成点播")
        pop.clicked.connect(self.pop_queue)
        insert_layout.addWidget(append)
        insert_layout.addWidget(push)
        insert_layout.addWidget(pop)
        insert.setLayout(insert_layout)
        
        insert_anywhere = QWidget(self)
        ia_layout = QHBoxLayout()
        insert_text1 = QLabel("向第", insert_anywhere)
        self.insert_place = QLineEdit(insert_anywhere)
        self.insert_place.setFixedWidth(50)
        insert_text2 = QLabel("行插入", insert_anywhere)
        insert_button = QPushButton(insert_anywhere)
        insert_button.setText("插入点播")
        insert_button.clicked.connect(self.insert_queue)
        ia_layout.addWidget(insert_text1)
        ia_layout.addWidget(self.insert_place)
        ia_layout.addWidget(insert_text2)
        ia_layout.addWidget(insert_button)
        insert_anywhere.setLayout(ia_layout)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(edit, alignment=Qt.AlignBottom)
        self.layout.addWidget(insert, alignment=Qt.AlignBottom)
        self.layout.addWidget(insert_anywhere, alignment=Qt.AlignBottom)
        
        self.setGeometry(0, 0, 960, 960)
        self.setLayout(self.layout)
        
        
    def construct_table(self, queue: deque[dict]) -> QTableWidget:
        table = QTableWidget(self)
        n = len(queue)
        table.setRowCount(n)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["老板名称", "点播内容", "点播时间"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        table.setColumnWidth(2, 150)
        for i in range(n):
            table.setItem(i, 0, QTableWidgetItem(queue[i]['name']))
            table.setItem(i, 1, QTableWidgetItem(queue[i]['desc']))
            table.setItem(i, 2, QTableWidgetItem(queue[i]['date']))
        return table

    def append_queue(self):
        self.insert_queue(self.table.rowCount())
        
    def push_queue(self):
        self.insert_queue(0)
        
    def pop_queue(self):
        self.history.popleft()
        self.table.removeRow(0)
    
    def insert_queue(self, row = None):
        name = self.name.toPlainText()
        desc = self.desc.toPlainText()
        date = self.date.toPlainText()
        new = {}
        new['name'] = name
        new['desc'] = desc
        new['date'] = date
        if row == None:
            # Inserting
            row = int(self.insert_place.toPlainText())
            self.history.insert(row, new)
        elif row == 0:
            # Pushing
            self.history.appendleft(new)
        elif row == self.table.rowCount():
            # Appending
            self.history.append(new)
        
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(desc))
        self.table.setItem(row, 2, QTableWidgetItem(date))
    
    def updateJSON(self):
        with open('history.json', "w") as h:
            h.write(json.dumps(list(self.history)))

    def __del__(self):
        self.updateJSON()
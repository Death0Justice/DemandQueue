from collections import deque
import csv, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QCursor
from PyQt5.QtCore import Qt, QPoint
        
class DemandQueue(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        if not self.initHistory():
            return
        self.initUI()
    
    def initHistory(self) -> bool:
        self.history = deque()
        try:
            with open('history.csv', "r", encoding="utf-8") as h:
                reader = csv.reader(h, delimiter=',')
                for line in reader:
                    self.history.append(line)
        except FileNotFoundError:
            with open('history.csv', "x", encoding="utf-8") as h:
                pass
        except:
            # Can be handled using a dialog window
            # print('File corrupted, recreating? Y/N')
            while True:
                prompt = input()
                if (prompt == 'y' or prompt == 'Y'):
                    with open('history.csv', "w", encoding="utf-8") as h:
                        pass
                    break
                elif (prompt == 'n' or prompt == 'N'):
                    return False
        return True
    
    def initUI(self):
            
        self.table = self.construct_table(self.history)
        
        # Constraint on self.insert_place
        self.onlyInt = QIntValidator(self)
        self.onlyInt.setRange(1, self.table.rowCount())
        
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
        quick = QPushButton(insert)
        quick.setText("快速添加")
        quick.clicked.connect(self.quick_action)
        append = QPushButton(insert)
        append.setText("添加点播")
        append.clicked.connect(self.append_queue)
        push = QPushButton(insert)
        push.setText("插播")
        push.clicked.connect(self.push_queue)
        pop = QPushButton(insert)
        pop.setText("完成点播")
        pop.clicked.connect(self.pop_queue)
        insert_layout.addWidget(quick)
        insert_layout.addWidget(append)
        insert_layout.addWidget(push)
        insert_layout.addWidget(pop)
        insert.setLayout(insert_layout)
        
        insert_anywhere = QWidget(self)
        ia_layout = QHBoxLayout()
        insert_text1 = QLabel("向第", insert_anywhere)
        self.insert_place = QLineEdit(insert_anywhere)
        self.insert_place.setFixedWidth(50)
        self.insert_place.setValidator(self.onlyInt)
        insert_text2 = QLabel("行", insert_anywhere)
        insert_button = QPushButton(insert_anywhere)
        insert_button.setText("插入点播")
        insert_button.clicked.connect(self.insert_anywhere)
        ia_layout.addStretch()
        ia_layout.addWidget(insert_text1)
        ia_layout.addWidget(self.insert_place)
        ia_layout.addWidget(insert_text2)
        ia_layout.addWidget(insert_button)
        ia_layout.addStretch()
        insert_anywhere.setLayout(ia_layout)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(edit, alignment=Qt.AlignBottom)
        self.layout.addWidget(insert, alignment=Qt.AlignBottom)
        self.layout.addWidget(insert_anywhere, alignment=Qt.AlignBottom)
        
        self.setGeometry(0, 0, 960, 960)
        self.setLayout(self.layout)
        
    def construct_table(self, queue: deque[list]) -> QTableWidget:
        table = QTableWidget(self)
        n = len(queue)
        table.setRowCount(n)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["老板名称", "点播内容", "点播时间"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        table.setColumnWidth(2, 150)
        table.cellDoubleClicked.connect(self.showDemand)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        for i in range(n):
            table.setItem(i, 0, QTableWidgetItem(queue[i][0]))
            table.setItem(i, 1, QTableWidgetItem(queue[i][1]))
            table.setItem(i, 2, QTableWidgetItem(queue[i][2]))
        return table
    
    def showDemand(self, row, col):
        demand = self.history[row]
        dialog = QDialog(self)
        dialog.setWindowTitle(f'点播详情')
        dialog.setMinimumSize(480, 270)
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(QLabel(f'{demand[0]}的点播'), alignment=Qt.AlignCenter)
        info = QLabel(demand[1], dialog)
        info.setWordWrap(True)
        dialog_layout.addWidget(info, alignment=Qt.AlignCenter)
        dialog_layout.addWidget(QLabel(f'于{demand[2]}', dialog), alignment=Qt.AlignCenter)
        dialog.setLayout(dialog_layout)
        dialog.exec()
        
    def insert_anywhere(self):
        self.insert_queue()

    def append_queue(self):
        self.insert_queue(self.table.rowCount())
        
    def push_queue(self):
        self.insert_queue(0)
        
    def pop_queue(self):
        if len(self.history) == 0:
            # Empty history
            # Can add pop-up here
            return
        self.history.popleft()
        self.table.removeRow(0)
        
        self.onlyInt.setTop(self.table.rowCount())
        self.updateCSV()
    
    def insert_queue(self, row=None):
        name = self.name.toPlainText()
        desc = self.desc.toPlainText()
        date = self.date.toPlainText()
        new = [name, desc, date]
        if row == None:
            # Inserting
            row = int(self.insert_place.text()) - 1
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
        
        self.onlyInt.setTop(self.table.rowCount())
        self.updateCSV()
    
    def quick_action(self):
        # Save the csv file before using buggy feature
        self.updateCSV()
        hint = "请输入以下格式点播：\n"
        hint += "[老板名称]\n"
        hint += "[点播内容]\n"
        hint += "[点播时间]\n"
        hint += "请用分号\";\"分隔多个点播\n"
        hint += "请注意：多个点播不支持插播"
        text, ok = QInputDialog.getMultiLineText(self, "快速输入", 
            hint)

        if ok:
            table = str(text).split(";")
            if len(table) > 1:
                for line in table:
                    if not line:
                        continue
                    row = [s for s in line.split("\n") if s]
                    # Appending
                    name = row[0]
                    date = row[-1]
                    desc = "\n".join(row[1:-1])
                    self.history.append(row)
                    n = self.table.rowCount()
                    self.table.insertRow(n)
                    self.table.setItem(n, 0, QTableWidgetItem(name))
                    self.table.setItem(n, 1, QTableWidgetItem(desc))
                    self.table.setItem(n, 2, QTableWidgetItem(date))
            else:
                row = [s for s in str(text).split("\n") if s]
                name = row[0]
                date = row[-1]
                desc = "\n".join(row[1:-1])
                self.name.setText(name)
                self.desc.setText(desc)
                self.date.setText(date)
        
        self.onlyInt.setTop(self.table.rowCount())
        self.updateCSV()
    
    def updateCSV(self):
        # print(self.history)
        with open('history.csv', "w", encoding="utf-8") as h:
            writer = csv.writer(h, delimiter=",", lineterminator="\n")
            for line in self.history:
                writer.writerow(line)
        
if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    window = QWidget()
    dq = DemandQueue(window)
    window.setWindowTitle("点播队列")
    window.resize(960, 960)
    window.show()
    
    sys.exit(qApp.exec_())
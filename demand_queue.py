from collections import deque
import csv, sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QCursor, QCloseEvent, QKeySequence
from PyQt5.QtCore import Qt, QPoint
        
class DemandQueue(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.date_format = '%Y-%m-%d %H:%M'
        self.initShortcut()
        if not self.initHistory():
            return
        self.initUI()
        
    def initShortcut(self):
        shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        shortcut.activated.connect(self.updateCSV)
        
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
        quick = QPushButton("快速添加", insert)
        quick.clicked.connect(self.quick_action)
        append = QPushButton("添加点播", insert)
        append.clicked.connect(self.append_queue)
        push = QPushButton("插播", insert)
        push.clicked.connect(self.push_queue)
        pop = QPushButton("完成点播", insert)
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
        insert_button = QPushButton("插入点播", insert_anywhere)
        insert_button.clicked.connect(self.insert_anywhere)
        sort_button = QPushButton("按时间排序")
        sort_button.clicked.connect(self.sort)
        delete_button = QPushButton("删除错误格式点播", insert_anywhere)
        delete_button.clicked.connect(self.del_unformatted)
        ia_layout.addStretch()
        ia_layout.addWidget(insert_text1)
        ia_layout.addWidget(self.insert_place)
        ia_layout.addWidget(insert_text2)
        ia_layout.addWidget(insert_button)
        ia_layout.addWidget(sort_button)
        ia_layout.addWidget(delete_button)
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
        table.setColumnWidth(2, 170)
        table.cellDoubleClicked.connect(self.showDemand)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        for i in range(n):
            table.setItem(i, 0, QTableWidgetItem(queue[i][0]))
            table.setItem(i, 1, QTableWidgetItem(queue[i][1]))
            table.setItem(i, 2, QTableWidgetItem(queue[i][2]))
        return table
    
    def showDemand(self, row, col):
        if col == 1:
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
    
    def del_unformatted(self):
        if len(self.history) == 0:
            return
        while not self.validate(self.history[-1][2]):
            self.history.pop()
            self.table.removeRow(self.table.rowCount() - 1)
        self.onlyInt.setTop(self.table.rowCount())
    
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
            new = [new[0], "插播: " + new[1], new[2]]
            self.history.appendleft(new)
        elif row == self.table.rowCount():
            # Appending
            self.history.append(new)
        
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(new[0]))
        self.table.setItem(row, 1, QTableWidgetItem(new[1]))
        self.table.setItem(row, 2, QTableWidgetItem(new[2]))
        
        self.onlyInt.setTop(self.table.rowCount())
    
    def quick_action(self):
        # # Save the csv file before using buggy feature
        # self.updateCSV()
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
                    self.history.append([name, desc, date])
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
    
    def sort(self):
        push_history = []
        append_history = []
        unformatted_history = []
        for h in self.history:
            if self.validate(h[2]):
                if str(h[1]).startswith("插播"):
                    push_history.append(h)
                else:
                    datetime.strptime(h[2], self.date_format)
                    append_history.append(h)
            else:
                unformatted_history.append(h)
        push_history.sort(key=lambda h: datetime.strptime(h[2], self.date_format), reverse=True)
        append_history.sort(key=lambda h: datetime.strptime(h[2], self.date_format))
        
        self.history = deque(push_history + append_history + unformatted_history)
        # print(self.history)
        self.table.clearContents()
        for i, h in enumerate(self.history):
            self.table.setItem(i, 0, QTableWidgetItem(h[0]))
            self.table.setItem(i, 1, QTableWidgetItem(h[1]))
            self.table.setItem(i, 2, QTableWidgetItem(h[2]))
        
        conclusion = QDialog(self)
        conclusion.setWindowTitle("排序结果")
        congrats = QLabel("排序完成！", conclusion)
        result = QLabel(f'发现{len(unformatted_history)}个格式错误的点播。', conclusion)
        conclusion_layout = QVBoxLayout()
        conclusion_layout.addWidget(congrats, alignment=Qt.AlignCenter)
        conclusion_layout.addWidget(result, alignment=Qt.AlignCenter)
        conclusion.setLayout(conclusion_layout)
        conclusion.setMinimumSize(480, 270)
        conclusion.exec()
    
    def updateCSV(self):
        # print(self.history)
        with open('history.csv', "w", encoding="utf-8") as h:
            writer = csv.writer(h, delimiter=",", lineterminator="\n")
            for line in self.history:
                writer.writerow(line)
    
    def validate(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, self.date_format)
            return True
        except:
            return False

    def closeEvent(self, e: QCloseEvent):
        reply = QMessageBox.question(self, '保存', '是否保存当前点播队列？', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        match reply:
            case QMessageBox.Yes:
                self.updateCSV()
                e.accept()
            case QMessageBox.No:
                e.accept()
            case QMessageBox.Cancel:
                e.ignore()
        
if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    dq = DemandQueue()
    dq.setWindowTitle("点播队列")
    dq.resize(960, 960)
    # Center the window
    qr = dq.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    dq.move(qr.topLeft())
    
    dq.show()
    
    sys.exit(qApp.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from demand_queue import DemandQueue

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    window = QWidget()
    dq = DemandQueue(window)
    window.setWindowTitle("点播队列")
    window.resize(960, 960)
    window.show()
    
    sys.exit(qApp.exec_())
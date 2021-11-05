import time
import sys
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon
from gameMainWindow import *
from block import *
from board import *
from generate_board import *
from search import *
from utils import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt


class ProcessMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ProcessMainWindow, self).__init__()
        self.setupUi(self)
        self.use_palette()
        self.board = Board(0,0,0,0)
        self.stack = Stack()
        self.display_tableWidget.horizontalHeader().setHidden(True)
        self.display_tableWidget.verticalHeader().setHidden(True)
        self.display_tableWidget.setShowGrid(False)
        self.display_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.init_tableWidget.horizontalHeader().setHidden(True)
        self.init_tableWidget.verticalHeader().setHidden(True)
        self.init_tableWidget.setShowGrid(False)
        self.init_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.total_turns_label.setText("total turns: 0")
        self.label.setHidden(True)

    def use_palette(self): 
        self.setWindowTitle("连连看")
        self.setWindowIcon(QIcon('./pictures/1.jpg'))
        window_pale = QtGui.QPalette() 
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./pictures/background.jpg"))) 
        self.setPalette(window_pale)

    def display_init_board(self):
        m = self.board.m
        n = self.board.n
        block_size = 70
        block_size_init_widget = 40
        if m > n:
            block_size = 400 //  m
            block_size_init_widget = 150 // m
        else:
            block_size = 400 //  n
            block_size_init_widget = 150 // n
        self.total_turns_label.setText("total turns: 0")
        self.label.setHidden(True)
        self.display_tableWidget.clear()
        self.display_tableWidget.setRowCount(m)
        self.display_tableWidget.setColumnCount(n)
        self.display_tableWidget.setFixedSize(n*block_size+2, m*block_size+2)
        for i in range(m):
            self.display_tableWidget.setRowHeight(i, block_size)
        for j in range(n):
            self.display_tableWidget.setColumnWidth(j, block_size)
        self.display_tableWidget.setIconSize(QSize(block_size-8, block_size-8))
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem()
                pattern = self.board.block_posi_list[i][j]
                item.setIcon(QIcon(QPixmap("./pictures/" + str(pattern) + ".jpg")))
                self.display_tableWidget.setItem(i, j, item)
        
        self.init_tableWidget.clear()
        self.init_tableWidget.setRowCount(m)
        self.init_tableWidget.setColumnCount(n)
        self.init_tableWidget.setFixedSize(n*block_size_init_widget+10, m*block_size_init_widget+10)
        for i in range(m):
            self.init_tableWidget.setRowHeight(i, block_size_init_widget)
        for j in range(n):
            self.init_tableWidget.setColumnWidth(j, block_size_init_widget)
        self.init_tableWidget.setIconSize(QSize(block_size_init_widget-5, block_size_init_widget-5))
        for i in range(m):
            for j in range(n):
                item = QTableWidgetItem()
                pattern = self.board.block_posi_list[i][j]
                item.setIcon(QIcon(QPixmap("./pictures/" + str(pattern) + ".jpg")))
                self.init_tableWidget.setItem(i, j, item)

    def assign_board_clicked(self):
        posi_list = []
        if self.assigned_board_textEdit.toPlainText() == '':
            posi_list = [
                [3, 0, 4, 3],
                [0, 2, 3, 3],
                [2, 3, 2, 0],
                [3, 2, 4, 0]
            ]
            # posi_list = [
            #     [-1, 2, 1],
            #     [2, -1, 1],
            #     [0, 2, 2],
            # ]
        else:
            posi_list = eval(self.assigned_board_textEdit.toPlainText())
        self.board = generate_assign_board(posi_list)
        self.display_init_board()

    def random_board_clicked(self):
        if self.m_lineEdit.text() != '':
            m = int(self.m_lineEdit.text())
        else:
            m = 3
        if self.n_lineEdit.text() != '':
            n = int(self.n_lineEdit.text())
        else:
            n = 4
        if self.k_lineEdit.text() != '':
            k = int(self.k_lineEdit.text())
        else:
            k = 6
        if self.p_lineEdit.text() != '':
            p = int(self.p_lineEdit.text())
        else:
            p = 4
        self.board = generate_random_board(m, n, k, p)
        self.display_init_board()

    def random_board_blocks_clicked(self):
        if self.m_lineEdit.text() != '':
            m = int(self.m_lineEdit.text())
        else:
            m = 3
        if self.n_lineEdit.text() != '':
            n = int(self.n_lineEdit.text())
        else:
            n = 4
        if self.k_lineEdit.text() != '':
            k = int(self.k_lineEdit.text())
        else:
            k = 6
        if self.p_lineEdit.text() != '':
            p = int(self.p_lineEdit.text())
        else:
            p = 4
        self.board = generate_random_board_blocks(m, n, k, p)
        self.display_init_board()
    
    def search_limit_clicked(self):
        if self.limit_lineEdit.text() != '':
            limit = int(self.limit_lineEdit.text())
        else:
            limit = 2
        final_board = Board(0, 0, 0, 0)
        if self.board.m * self.board.n > 20:
            final_board = bfs_with_limit_prior_connect(self.board, limit)
        else:
            final_board = bfs_with_limit(self.board, limit)
        self.label.setHidden(False)
        while self.stack.empty() == False:
            stack.pop()
        while final_board != None:
            self.stack.push(final_board)
            final_board = final_board.parent

    def search_no_limit_clicked(self):
        final_board = Board(0, 0, 0, 0)
        if self.board.m * self.board.n > 20:
            final_board = bfs_without_limit_prior_connect(self.board)
        else:
            final_board = bfs_without_limit(self.board)
        self.label.setHidden(False)
        while self.stack.empty() == False:
            self.stack.pop()
        while final_board != None:
            self.stack.push(final_board)
            final_board = final_board.parent
    
    def display_path_clicked(self):
        if self.stack.empty() == False:
            self.board = self.stack.pop()
            if self.board.parent == None and self.stack.empty() == False:
                self.board = self.stack.pop()
            self.display()

    def display(self):
        self.total_turns_label.setText("total turns: %d" % self.board.total_turns)
        for i in range(self.board.m):
            for j in range(self.board.n):
                item = QTableWidgetItem()
                pattern = self.board.block_posi_list[i][j]
                item.setIcon(QIcon(QPixmap("./pictures/" + str(pattern) + ".jpg")))
                self.display_tableWidget.setItem(i, j, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ProcessMainWindow()
    game.paintEngine()
    game.show()
    sys.exit(app.exec_())

from processMainWindow import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.Qt import *

def main():
    app = QApplication(sys.argv)
    game = ProcessMainWindow()
    game.paintEngine()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
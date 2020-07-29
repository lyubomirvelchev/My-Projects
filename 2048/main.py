import sys
from PyQt5.QtWidgets import QApplication

from game2048 import GameClassCombined

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameClassCombined(size=4)
    sys.exit(app.exec_())
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from UI.tile import TileBase
from UI.common import FakeCallable, STYLE_SHEET, CellsColors


class KeysMixin:
    def __init__(self):
        super(KeysMixin, self).__init__()
        self.keys_map = {
            QtCore.Qt.Key_Up: self.arrow_up_callback,
            QtCore.Qt.Key_Down: self.arrow_down_callback,
            QtCore.Qt.Key_Left: self.arrow_left_callback,
            QtCore.Qt.Key_Right: self.arrow_right_callback
        }

    def arrow_up_callback(self):
        print('up')

    def arrow_down_callback(self):
        print('down')

    def arrow_left_callback(self):
        print("left")

    def arrow_right_callback(self):
        print('right')

    def keyPressEvent(self, QKeyEvent):
        self.keys_map.get(QKeyEvent.key(), FakeCallable())()


class UI2048Base(KeysMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, size=4, window_size=500, **kwargs):
        super(UI2048Base, self).__init__(*args, **kwargs)
        self.setFixedSize(window_size,window_size)

        self.board_size = size

        self.init_ui()

    def init_ui(self):
        self.setup_layout()
        self.setStyleSheet(STYLE_SHEET.format(*CellsColors.COLOR_GAME.value))
        self.show()

    def set_grid(self,grid):
        self.central.set_grid(grid)

    def get_grid(self):
        return self.central.get_grid()

    def set_game_over_screen(self):
        pass

    def setup_layout(self):
        self.central = CentralWidget(self, grid_size=self.board_size)
        self.setCentralWidget(self.central)


class CentralWidget(QtWidgets.QWidget):
    def __init__(self,  *args, grid_size=4, **kwargs):
        super(CentralWidget, self).__init__(*args, **kwargs)
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.grid_size = grid_size
        self.new_grid()

    def new_grid(self):
        for ridx in range(self.grid_size):
            for cidx in range(self.grid_size):
                tile = TileBase(value=0)
                self.grid_layout.addWidget(tile,ridx,cidx)

    def set_grid(self, grid):
        for ridx, row in enumerate(grid):
            for cidx, elem in enumerate(row):
                tile = self.grid_layout.itemAtPosition(ridx, cidx).widget()
                tile.set_value(elem)

    def get_grid(self):
        return [[
                    self.grid_layout.itemAtPosition(row, col).widget().value_label.text()
                    for col in range(self.grid_size)
                 ]
                for row in range(self.grid_size)]




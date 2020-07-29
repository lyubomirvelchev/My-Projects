from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from UI.common import STYLE_SHEET, KEY_STRING, CellsColors


class NoZerolabel(QtWidgets.QLabel):
    def text(self):
        text = super(NoZerolabel, self).text()
        if text == ' ':
            return 0
        return text


class TileBase(QtWidgets.QWidget):
    def __init__(self, *args,value=0, **kwargs):
        super(TileBase, self).__init__(*args, **kwargs)

        self.value_label = NoZerolabel(self)
        self.value_label.setAlignment(Qt.AlignCenter)

        self.value_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)

        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0,0,0,0)

        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox.addLayout(self.vbox, )

        self.vbox.addWidget(self.value_label)

        self.setLayout(self.hbox)

        self.set_value(value)
        self.show()

    def set_value(self, val):
        col = getattr(CellsColors, KEY_STRING.format(str(val)), CellsColors.COLOR_0)

        self.value_label.setText(str(val if val != 0 else ' '))
        self.setStyleSheet(STYLE_SHEET.format(*col.value))

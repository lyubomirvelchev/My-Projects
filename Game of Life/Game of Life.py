from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QVBoxLayout, \
    QLabel, QSlider, \
    QHBoxLayout
from PyQt5.QtCore import Qt
import sys
import random


class Cell(QLabel):
    def __init__(self):
        super().__init__()
        self.state = 0  # default state

    def switch_state(self):
        """Changes the state of the cell"""
        if self.state == 0:
            self.state = 1
            self.apply_colour()
        else:
            self.state = 0
            self.apply_colour()

    def apply_colour(self):
        """Changes the colour of the cell according to its state"""
        if self.state == 0:
            self.setStyleSheet("background-color:white;")
        else:
            self.setStyleSheet("background-color:black;")

    def mousePressEvent(self, QMouseEvent):
        """Changes the state of the cell and immideately applies the change into the matrix"""
        self.switch_state()
        self.parent().board_to_matrix()


class Slider(QSlider):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Vertical)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setMinimum(0)
        self.setMaximum(9)
        self.setTickPosition(1)
        self.slider_values_dictionary = {  # slider values
            0: 2000,
            1: 1500,
            2: 1000,
            3: 750,
            4: 400,
            5: 200,
            6: 100,
            7: 50,
            8: 20,
            9: 10,
        }

    def get_norm_value(self):
        return self.slider_values_dictionary.get(self.value(), 2000)


class GameOfLife(QWidget):
    def __init__(self, width=10, height=10):
        super().__init__()
        self.matrix = [[0 for x in range(width)] for y in range(height)]
        self.buffer_matrix = [[0 for x in range(width)] for y in range(height)]
        self.cell_width = 20
        self.cell_height = 20
        self.InitWindow((width * self.cell_width + 75), (
                height * self.cell_height + 20))  # resizes the window so that it makes the cells relatively rectangular
        self.board = QGridLayout()  # displays all the cells
        self.cells = []  # stores all the cells
        self.init_grid()
        self.slider = Slider()
        self.slider.sliderReleased.connect(self.slider_event)
        self.speed = self.slider.get_norm_value()
        self.speed_label = QLabel(str(self.speed) + "ms")
        self.init_pauseStart_button()
        self.matrix_to_board()
        self.board_to_matrix()
        # self.set_random_grid()  #uncomment if you want to generate a random filled grid
        self.horizontal_box_layout()
        self.vertical_box_layout()

        self.timer_id = self.startTimer(self.speed)

    def set_random_grid(self):
        for cell in self.cells:
            state = random.randint(0, 1)
            cell.state = state
            cell.apply_colour()


    def init_pauseStart_button(self):
        self.pause_button = QPushButton("Pause")
        self.pause_button.setCheckable(True)
        self.pause_button.clicked.connect(self.click_event)

    def timerEvent(self, QTimerEvent):
        """Applies the algorithm every time frame and makes sure the board and the matrix have the same values"""
        self.board_to_matrix()
        self.game_fo_life_algorithm()
        self.matrix_to_board()


        self.buffer_matrix = [[0 for x in range(len(self.matrix[0]))] for y in
                              range(len(self.matrix))]  # reset buffer matrix

    def click_event(self):
        if self.pause_button.isChecked():
            self.killTimer(self.timer_id)
            self.pause_button.setText("Start")
        else:
            self.killTimer(self.timer_id)
            self.speed = self.slider.get_norm_value()
            self.timer_id = self.startTimer(self.speed)  # applies the correct refresh rate
            self.pause_button.setText("Pause")

    def slider_event(self):
        self.killTimer(self.timer_id)
        self.speed = self.slider.get_norm_value()
        self.speed_label.setText(str(self.speed) + "ms")
        if not self.pause_button.isChecked():
            self.timer_id = self.startTimer(self.speed)  # applies the correct refresh rate aster the slider is moved

    def InitWindow(self, hor_size, ver_size):
        self.setWindowTitle("Cellular Integration")  # not the correct name but it sounds kinda cool
        self.setGeometry(300, 100, hor_size, ver_size)

    def init_grid(self):
        """Creates a 2d list full of zeros and a board full of white cells"""
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                square = Cell()
                square.state = 0
                square.apply_colour()
                self.board.addWidget(square, row, column)
                self.cells.append(square)

    def matrix_to_board(self):
        """Applies the values in the matrix into the cells"""
        counter = 0
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                self.cells[counter].state = self.matrix[row][column]
                self.cells[counter].apply_colour()
                counter += 1

    def board_to_matrix(self):
        """Applies the stata of the cells into the matrix"""
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                self.matrix[row][column] = self.board.itemAtPosition(row, column).widget().state

    def horizontal_box_layout(self):
        """Some basic UI layout"""
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.board)
        self.hbox.addWidget(self.slider)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.pause_button)
        self.hbox2.addWidget(self.speed_label)

    def vertical_box_layout(self):
        """Some basic UI layout"""
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)
        self.show()

    def get_neightbours(self, row, column):
        """Finds all the adjacent cells of a given cell and returns them in a list"""
        """The congruence used handles all the corner cases"""
        neightbours = []
        neightbours.append(self.matrix[(row - 1) % len(self.matrix)][(column - 1) % len(self.matrix[0])])
        neightbours.append(self.matrix[(row - 1) % len(self.matrix)][column % len(self.matrix[0])])
        neightbours.append(self.matrix[(row - 1) % len(self.matrix)][(column + 1) % len(self.matrix[0])])
        neightbours.append(self.matrix[row % len(self.matrix)][(column - 1) % len(self.matrix[0])])
        neightbours.append(self.matrix[row % len(self.matrix)][(column + 1) % len(self.matrix[0])])
        neightbours.append(self.matrix[(row + 1) % len(self.matrix)][(column - 1) % len(self.matrix[0])])
        neightbours.append(self.matrix[(row + 1) % len(self.matrix)][column % len(self.matrix[0])])
        neightbours.append(self.matrix[(row + 1) % len(self.matrix)][(column + 1) % len(self.matrix[0])])
        return neightbours

    def if_cases(self, row, column, neightbours):
        """These are the rules of Game of Life"""
        if self.matrix[row][column] == 1:
            if sum(neightbours) < 2 or sum(neightbours) > 3:
                self.buffer_matrix[row][column] = 0
            else:
                self.buffer_matrix[row][column] = 1
        else:
            if sum(neightbours) == 3:
                self.buffer_matrix[row][column] = 1

    def game_fo_life_algorithm(self):
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                self.if_cases(row, column, self.get_neightbours(row, column))  # applies the rules for each cell
        self.matrix = self.buffer_matrix  # the real matrix gets all the values and after that the buffer matrix is reset


App = QApplication(sys.argv)
window = GameOfLife(30,25)
sys.exit(App.exec())

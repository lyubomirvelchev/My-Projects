from glob import glob
from PyQt5.QtGui import QPixmap, QTransform

from PyQt5 import QtCore
import math

IMAGES_PATH = r"./images/"


class SpriteMixin:
    """this mixin divides a spritesheet into frames and applies the chosen frame"""
    def __init__(self, *args, frames_x=8, frames_y=8, offset=(0, 0), **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = self.__class__.__name__
        self.number_frames_X = frames_x
        self.number_frames_Y = frames_y
        self.image_pixmap = QPixmap(self.find_image())
        self.horizontal_starting_offset = offset[0]
        self.vertical_starting_offset = offset[1]
        self.X_frame_size = int((self.image_pixmap.width() - 2 * self.horizontal_starting_offset) / frames_x)
        self.Y_frame_size = int((self.image_pixmap.height() - 2 * self.vertical_starting_offset) / frames_y)
        self.current_frame = (0, 0)
        self.set_frame(*self.current_frame)

    def find_image(self):
        return glob(IMAGES_PATH + self.class_name + "Sprite" + '.*')[0]

    def calculate_frames(self, x, y):
        """calculates the starting point of the new frame"""
        x_start = self.horizontal_starting_offset + x * self.X_frame_size
        y_start = self.vertical_starting_offset + y * self.Y_frame_size
        return x_start, y_start

    def set_frame(self, x, y):
        """cuts the correct frame with the correct size"""
        new_image = self.image_pixmap.copy(*self.calculate_frames(x, y), self.X_frame_size, self.Y_frame_size)
        a = new_image.scaled(self.size())
        self.setPixmap(a)
        self.current_frame = (x, y)

    def resizeEvent(self, QResizeEvent): # this is needed when the label gets rotated
        super().resizeEvent(QResizeEvent)
        self.resize(QResizeEvent.size())
        self.set_frame(*self.current_frame)


class ImageMixin:
    """Must be inherited by with QWidget class."""
    rotation_degree = 0

    def __init__(self, *args, rotation_speed=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = self.__class__.__name__
        self.original_pixmap = QPixmap(self.find_image())
        self.setPixmap(self.original_pixmap)
        self.object_angle = 0
        self.rotation_speed = rotation_speed

    def find_image(self):
        return glob(IMAGES_PATH + self.class_name + '.*')[0]

    def set_rotation(self, deg):
        self.rotation_degree = deg
        self.update_angle()

    def get_rotation(self):
        return self.rotation_degree

    def get_angle(self):
        return self.object_angle

    def rotate(self, deg): # rotate and handle the angle transition from 360 to 0 and reverse
        self.set_rotation(self.get_rotation() + deg)
        if self.object_angle + deg < 0:
            self.object_angle += deg + 360
        elif self.object_angle + deg > 360:
            self.object_angle += deg - 360
        else:
            self.object_angle += deg

    def update_angle(self):
        """ Transforms the image based on the angle"""
        pix = self.original_pixmap
        t = QTransform().rotate(self.rotation_degree)
        rotated = pix.transformed(t)
        xoffset = (rotated.width() - pix.width()) / 2
        yoffset = (rotated.height() - pix.height()) / 2
        rotated = rotated.copy(xoffset, yoffset, pix.width(), pix.height())
        self.setPixmap(rotated.scaled(self.size()))
        self.update()

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.resize(QResizeEvent.size())
        self.update_angle()


class MoveMixin:
    def __init__(self, *args, rotation_speed=0, angle=0, max_speed=0, current_speed=0, coord_x=0, coord_y=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.sin_cos = [0, 0.01745, 0.03490, 0.05234, 0.06976, 0.08716, 0.10453, 0.12187, 0.13917, 0.15643, 0.17365,
                        0.19081, 0.20791, 0.22495, 0.24192, 0.25882, 0.27564, 0.29237, 0.30902, 0.32557, 0.34202,
                        0.35837, 0.37461, 0.39073, 0.40674, 0.42262, 0.43837, 0.45399, 0.46947, 0.48481, 0.5, 0.51504,
                        0.52992, 0.54464, 0.55919, 0.57358, 0.58779, 0.60182, 0.61566, 0.62932, 0.64279, 0.65606,
                        0.66913, 0.68200, 0.69466, 0.70711,
                        0.71934, 0.73135, 0.74314, 0.75471, 0.76604, 0.77715, 0.78801, 0.79864, 0.80902, 0.81915,
                        0.82904, 0.83867, 0.84805, 0.85717, 0.86603, 0.87462, 0.88295, 0.89101, 0.89879, 0.90631,
                        0.91355, 0.92050, 0.92718, 0.93358, 0.93969, 0.94552, 0.95106, 0.95630, 0.96126, 0.96593,
                        0.97030, 0.97437, 0.97815, 0.98163, 0.98481, 0.98769, 0.99027, 0.99255, 0.99452, 0.99619,
                        0.99756, 0.99863, 0.99939, 0.99985, 1] # all sin/cos values between 0 and 90 degrees
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.object_angle = angle
        self.coord_1 = coord_x
        self.coord_2 = coord_y
        self.move(self.coord_1, self.coord_2)
        self.rounding_mistake_a = 0
        self.rounding_mistake_b = 0
        self.rotation_speed = rotation_speed
        self.zero_gravity = False

    def set_angle(self, deg):
        self.object_angle = deg

    def get_correct_sin(self, deg):
        """Chooses the correct value based on the angle"""
        if deg <= 90:
            return self.sin_cos[deg]
        elif deg <= 180:
            return self.sin_cos[180 - deg]
        elif deg <= 270:
            return -self.sin_cos[deg - 180]
        else:
            return -self.sin_cos[360 - deg]

    def get_correct_cos(self, deg):
        """Chooses the correct value based on the angle"""
        if deg <= 90:
            return self.sin_cos[90 - deg]
        elif deg <= 180:
            return -self.sin_cos[deg - 90]
        elif deg <= 270:
            return -self.sin_cos[270 - deg]
        else:
            return self.sin_cos[deg - 270]

    def end_to_end_transition(self):
        """Makes the ship and the asteroids to show from the opposite side of the screen when they hide from sight"""
        if self.coord_1 < -100:
            self.coord_1 = self.parent().width
        if self.coord_1 > self.parent().width + 100:
            self.coord_1 = -100
        if self.coord_2 < -100:
            self.coord_2 = self.parent().height
        if self.coord_2 > self.parent().height + 100:
            self.coord_2 = -100

    def forward_move(self, angle, speed):
        """Calculates the new coordinates based on the angle and the speed"""
        a1 = int(round(self.get_correct_sin(angle) * speed + self.rounding_mistake_a))
        b1 = int(round(self.get_correct_cos(angle) * speed + self.rounding_mistake_b))
        self.rounding_mistake_a += (self.get_correct_sin(angle) * speed) - a1
        self.rounding_mistake_b += (self.get_correct_cos(angle) * speed) - b1
        change_X = int(round(self.get_correct_sin(angle) * speed + self.rounding_mistake_a))
        change_Y = int(round(self.get_correct_cos(angle) * speed + self.rounding_mistake_b))
        self.coord_1 = self.coord_1 + change_X
        self.coord_2 = self.coord_2 - change_Y
        self.end_to_end_transition() # transition if needed
        self.current_moving_angle = angle
        return self.coord_1, self.coord_2



class FakeCallable:
    def __call__(self, *args, **kwargs):
        pass


class KeysMixin:
    USE_CALLBACKS = False

    def __init__(self):
        super(KeysMixin, self).__init__()
        self.keys_map = {
            QtCore.Qt.Key_Up: self.arrow_up_callback,
            QtCore.Qt.Key_Down: self.arrow_down_callback,
            QtCore.Qt.Key_Left: self.arrow_left_callback,
            QtCore.Qt.Key_Right: self.arrow_right_callback,
            QtCore.Qt.Key_Space: self.space_callback
        }

        self.keys_pressed = {
            QtCore.Qt.Key_Up: False,
            QtCore.Qt.Key_Down: False,
            QtCore.Qt.Key_Left: False,
            QtCore.Qt.Key_Right: False,
            QtCore.Qt.Key_Space: False
        }

    def arrow_up_callback(self):
        print('up')

    def arrow_down_callback(self):
        print('down')

    def arrow_left_callback(self):
        print("left")

    def arrow_right_callback(self):
        print('right')

    def space_callback(self):
        print(" ")

    def keyPressEvent(self, QKeyEvent):
        if self.USE_CALLBACKS:
            self.keys_map.get(QKeyEvent.key(), FakeCallable())()

        if QKeyEvent.key() in self.keys_pressed.keys():
            self.keys_pressed[QKeyEvent.key()] = True

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() in self.keys_pressed.keys():
            self.keys_pressed[QKeyEvent.key()] = False

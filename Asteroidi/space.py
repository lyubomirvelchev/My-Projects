import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Asteroidi.utils.mixins import ImageMixin, KeysMixin, MoveMixin, SpriteMixin
import random
import math


def forceful_angle_handling(angle):   # handle angle transition from 360 to 0 and reverse
    if angle < 0:
        return 360 + angle
    elif angle >= 360:
        return angle - 360
    else:
        return angle


class GameOver(ImageMixin, QLabel): # Game Over screen
    pass


class GameWon(ImageMixin, QLabel): # Victory screen
    pass


class SpaceBackground(ImageMixin, QLabel): # backgroud screen
    pass


class Explosion(SpriteMixin, QLabel): # handles the explosion if an asteroid or the ship are destroyed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, frames_x=8, frames_y=6, **kwargs)
        self.list_of_frames = [(x, y) for y in range(self.number_frames_Y) for x in range(self.number_frames_X)]
        self.frame_counter = 0

    def change_frame(self): # chooses the next frame of the spritesheet
        self.set_frame(self.list_of_frames[self.frame_counter][0], self.list_of_frames[self.frame_counter][1])
        self.frame_counter += 1
        if self.frame_counter == self.number_frames_X * self.number_frames_Y: # resets the counter
            self.frame_counter = 0


class Ship(SpriteMixin, MoveMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, frames_x=6, frames_y=6, **kwargs)
        self.list_of_frames = [(x, y) for y in range(6) for x in range(6)]
        self.list_of_angles = [x * 10 for x in range(37)]
        self.object_angle = 0
        self.vx, self.vy = 0, 0
        # print(self.list_of_frames)

    def rotate(self, angle):
        self.object_angle = forceful_angle_handling(angle + self.object_angle)

    def change_frame(self): # chooses the correct frame, based on the ship direction,based on the angle
        if self.object_angle == 0:
            self.set_frame(0, 0)
        else:
            for idx in range(36):
                if self.list_of_angles[idx] <= self.object_angle < self.list_of_angles[idx + 1]:
                    self.set_frame(self.list_of_frames[idx][0], self.list_of_frames[idx][1])

    def set_acceleration(self, acceleration):
        self.overall_acceleration = acceleration

    def make_speed_changes(self): # calculates the change in acceleration and applies that on the speed
        vx_change = self.current_speed * self.get_correct_sin(self.object_angle)
        vy_change = self.current_speed * self.get_correct_cos(self.object_angle)
        if (abs(self.vx) + abs(self.vy)) < 8:
            self.vx += vx_change
            self.vy += vy_change
        else:
            self.vx += vx_change
            self.vy += vy_change
            while (abs(self.vx) + abs(self.vy)) >= 8:
                self.vx = self.vx * 0.995
                self.vy = self.vy * 0.995






    def process_speed(self):
        if self.overall_acceleration > 0:
            if self.current_speed + self.overall_acceleration > self.max_speed:
                self.current_speed = self.max_speed # speed limit
            else:
                self.current_speed += self.overall_acceleration # change current speed
            self.make_speed_changes()

        else: # decrease the speed of the ship when the acceleration is not possitive
            self.vx *= 0.995
            self.vy *= 0.995


        self.coord_1 += self.vx
        self.coord_2 -= self.vy
        self.end_to_end_transition() # makes the ship stay withtin the screen
        self.move(self.coord_1, self.coord_2)


class Asteroid(SpriteMixin, MoveMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, frames_x=6, frames_y=5, **kwargs)
        self.set_angle(random.randint(0, 359)) # choose angle of velocity
        self.frame_counter = 0
        self.rotation_counter = 0

    def change_frame(self):  # choose correct frame from the spritesheet
        new_x = self.frame_counter % 6
        new_y = self.frame_counter // 6
        self.set_frame(new_x, new_y) # changes the frame
        self.frame_counter = self.frame_counter + 1 if self.frame_counter + 1 < 30 else 0

    def process_event(self): # applies the movement and the rotation of the asteroid
        coords = self.forward_move(self.object_angle, self.current_speed)
        self.move(coords[0], coords[1])
        if self.rotation_counter == 0:
            self.change_frame()
        self.rotation_counter = self.rotation_counter + 1 if self.rotation_counter + 1 < self.rotation_speed else 0


class Projectile(ImageMixin, MoveMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(6, 10)
        self.current_X = 0
        self.current_Y = 0

    def find_coord(self):
        self.current_X = self.forward_move(self.object_angle, self.current_speed)[0]
        self.current_Y = self.forward_move(self.object_angle, self.current_speed)[1]

    def execute_shooting(self):
        self.move(self.current_X, self.current_Y)
        self.show()


class BaseClass(QMainWindow, KeysMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 1920
        self.height = 1080
        self.InitWindow()
        self.set_background()
        self.set_ship()
        self.bunch_of_ast = self.set_asteroids()
        self.ship.change_frame()
        self.projectiles = []
        self.projectile_counter = 0
        self.explosion_list = []
        self.ship_collision = False
        self.lifes = 3
        self.ship_immunity_counter = 0
        self.game_over_label = GameOver(self)
        self.game_over_label.hide()
        self.game_won_label = GameWon(self)
        self.game_won_label.hide()
        self.show()
        self.update()

        self.startTimer(10)

    def timerEvent(self, QTimerEvent):

        if self.bunch_of_ast == []:
            self.game_won() # victory  condition: no asteroids left

        for asteroid in self.bunch_of_ast:
            asteroid.process_event()

        self.process_projectiles()
        self.display_explosions()
        self.handle_collision()
        self.rotate_ship(-3, Qt.Key_Left)  # rotate if the key is pressed
        self.rotate_ship(3, Qt.Key_Right)  # rotate if the key is pressed
        self.ship_acceleration()
        self.ship.process_speed()
        self.set_ship_immunity()

        if self.keys_pressed[Qt.Key_Space]: # doesnt let the player spam projectiles
            if self.projectile_counter == 50: # 1 projectile every 50 time frames
                self.projectile_counter = 0
            else:
                self.projectile_counter += 1
        else:
            self.projectile_counter = 0

    def InitWindow(self): # creates the window
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("SpaceWars")
        self.setWindowIcon(QIcon(r"./images/big_space.jpg"))

    def set_ship(self): # places the ship
        self.ship = Ship(self, angle=0, max_speed = 0.04, coord_x=500, coord_y=400)
        self.ship.resize(100, 100)

    def ship_acceleration(self):
        if self.keys_pressed[Qt.Key_Up]:
            self.ship.set_acceleration(0.009)
        else:
            self.ship.set_acceleration(-0.003)

    def set_background(self):
        self.background_img = SpaceBackground(self)
        self.background_img.resize(self.size())
        self.background_img.move(0, 0)

    def game_over(self):
        self.game_over_label.resize(1000, 400)
        self.game_over_label.move(500, 300)
        self.game_over_label.show()

    def game_won(self):
        self.game_won_label.resize(700, 400)
        self.game_won_label.move(700, 300)
        self.game_won_label.show()

    def set_ship_immunity(self): # makes the ship invulnerable immediately after being hit by asteroid
        if self.ship_immunity_counter != 0:
            self.ship_collision_reset()
            if self.ship_immunity_counter % 16 < 6 and self.ship_immunity_counter != 0: # makes the ship blink during immunity duratation
                self.ship.hide()
            else:
                self.ship.show()
            if self.lifes == 0: # hide the ship if it has no more lifes
                self.ship.hide()

    def process_projectiles(self):
        if self.keys_pressed[Qt.Key_Space] and self.projectile_counter == 0:
            self.add_projectile()
        for elem in self.projectiles:
            elem.find_coord()
            """Use the coordinates from the parent window. Be more abstract."""
            if elem.current_X < -50 or elem.current_X > self.width + 50 or elem.current_Y < -50 or elem.current_Y > self.height + 50:
                elem.hide()
                self.projectiles.remove(elem)
                del elem # removes projectile when it leaves the InitWindow
            else:
                elem.execute_shooting() # moves the projectile

    def ship_collision_reset(self):
        self.ship_immunity_counter += 1
        if self.ship_immunity_counter == 301: # about 3 seconds of ship immunity
            self.ship_immunity_counter = 0
            self.ship_collision = False

    def rotate_ship(self, deg, key): # rotates the ship based on the angle: "deg" and the key pressed
        if self.keys_pressed[key]:
            self.ship.rotate(deg)
            self.ship.change_frame()

    def display_explosions(self):
        pop_indx = 0
        for idx in range(len(self.explosion_list)):
            expl = self.explosion_list[idx - pop_indx]
            expl.change_frame()
            if expl.frame_counter == 0: #removes the explosion after it was fully displayed
                expl.hide()
                self.explosion_list.pop(idx)
                del expl
                pop_indx += 1

    def check_colision(self, asteroid, object_X_coord, object_Y_coord, object_radius):
        """Goes through every asteroid and checks if a projectile or the ship are close enough to the asteroid"""
        ast_radius = asteroid.width() / 2
        ast_center = (asteroid.coord_1 + ast_radius, asteroid.coord_2 + ast_radius)
        catet_1 = object_X_coord - ast_center[0]
        catet_2 = object_Y_coord - ast_center[1]
        distance = int(math.sqrt(catet_1 ** 2 + catet_2 ** 2))
        if distance < object_radius + ast_radius: # if the distance between the two obejcts is smaller than the sum of radiuses
            exp = Explosion(self)
            exp.resize(200, 200)
            exp.show()
            self.explosion_list.append(exp)
            return exp
        return None

    def handle_collision(self):
        """Applies the explosion and removes asteroids or the ship if needed"""
        ship_radius = self.ship.width() / 2 - 20
        ship_center = (self.ship.coord_1 + ship_radius, self.ship.coord_2 + ship_radius)
        if not self.ship_collision and self.lifes != 0:
            for asteroid in self.bunch_of_ast:
                expl = self.check_colision(asteroid, ship_center[0], ship_center[1], ship_radius)
                if expl != None:
                    self.ship_explosion(expl)
        for asteroid in self.bunch_of_ast: # collision check between each asteroid and each projectile
            for proj in self.projectiles:
                expl = self.check_colision(asteroid, proj.coord_1, proj.coord_2, 0)
                if expl != None:
                    self.projectiles.remove(proj)
                    proj.hide()
                    del proj
                    self.asteroid_explosion(asteroid, expl)
                    break

    def ship_explosion(self, expl):
        expl.move(self.ship.coord_1, self.ship.coord_2)
        self.ship_collision = True
        self.lifes -= 1
        self.ship_immunity_counter += 1
        if self.lifes == 0:
            self.ship.hide()
            self.game_over()

    def asteroid_explosion(self, asteroid, expl):
        """Splits the asteroid in smaller asteroids"""
        expl.move(asteroid.coord_1, asteroid.coord_2)
        asteroid.hide()
        if asteroid.width() == 110 or asteroid.height() == 160:
            ast_1_angle = asteroid.object_angle + 20 if asteroid.object_angle < 340 else asteroid.object_angle - 340 # splits the angle of the 2 new asteroids
            ast_2_angle = asteroid.object_angle - 20 if asteroid.object_angle >= 20 else asteroid.object_angle + 340
            ast_speed = random.randint(2, 4)
            ast_size = 60 if asteroid.width() == 110 else 110
            size_to_rotation_dict = { # the rotation speed of the asteroid is based on its size
                60: 2,
                110: 5,
                160: 8
            }
            rotation_speed = size_to_rotation_dict[ast_size]
            """Generates 2 new asteroids"""
            ast_1 = Asteroid(self, angle=ast_1_angle, max_speed=ast_speed, current_speed=ast_speed,
                             coord_x=asteroid.coord_1, coord_y=asteroid.coord_2, rotation_speed=rotation_speed)
            ast_2 = Asteroid(self, angle=ast_2_angle, max_speed=ast_speed, current_speed=ast_speed,
                             coord_x=asteroid.coord_1, coord_y=asteroid.coord_2, rotation_speed=rotation_speed)
            ast_1.object_angle = ast_1_angle
            ast_2.object_angle = ast_2_angle
            self.bunch_of_ast.append(ast_1)
            self.bunch_of_ast.append(ast_2)
            ast_1.resize(ast_size, ast_size)
            ast_2.resize(ast_size, ast_size)
            ast_1.show()
            ast_2.show()
        self.bunch_of_ast.remove(asteroid) # removes the asteroid that was hit

    def resizeEvent(self, QResizeEvent):
        super(BaseClass, self).resizeEvent(QResizeEvent)
        self.background_img.resizeEvent(QResizeEvent)

    def asteroid_dictionary(self):
        """This should be made relative to the current position of the ship. It will move after all."""
        x = random.randint(0, self.width)
        if x > 300 and x < 700: # spawn new asteroids in realtive distance to the ship
            numbers = random.randint(0, 300)
            numbers_2 = random.randint(700, self.height)
            y = random.choice([numbers, numbers_2])
        else:
            y = random.randint(0, self.height)
        speed = random.randint(1, 4)
        dictionary = {
            "angle": random.randint(0, 359),
            "max_speed": speed,
            "current_speed": speed,
            "coord_x": x,
            "coord_y": y
        }

        return dictionary

    def set_asteroids(self):
        """Asteroid factory that uses the astroid dictionary to spawn new asteroids"""
        names = []
        for number in range(10):
            size = random.choice([60, 110, 160])
            size_to_rotation_dict = {
                60: 2,
                110: 5,
                160: 8
            }
            rotation_speed = size_to_rotation_dict[size] # the rotation speed is relative to the size
            temp_ast = Asteroid(self, rotation_speed=rotation_speed, **self.asteroid_dictionary())
            temp_ast.resize(size, size)
            names.append(temp_ast)
        return names

    def add_projectile(self):
        """Projectile Factory"""
        angle = self.ship.object_angle
        coord_x = self.ship.coord_1
        coord_y = self.ship.coord_2
        proj = Projectile(self, angle=angle, max_speed=8, current_speed=8, coord_x=coord_x + 50, coord_y=coord_y + 50)
        proj.rotate(angle)
        self.projectiles.append(proj)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BaseClass()
    sys.exit(app.exec_())

from UI.UI import UI2048Base
from Game2048_v2 import GameClass


class GameClassCombined(UI2048Base, GameClass,):
    does_print = False

    def __init__(self, *args, **kwargs):
        super(GameClassCombined, self).__init__(*args, **kwargs)
        self.set_grid(self.board)

    def arrow_up_callback(self):
        self._on_turn('w')

    def arrow_down_callback(self):
        self._on_turn('s')

    def arrow_left_callback(self):
        self._on_turn('a')

    def arrow_right_callback(self):
        self._on_turn('d')

    def _on_turn(self, dir):
        self.execute_turn_if_possible(dir)
        self.set_grid(self.board)
        if not self.game_over():
            self.set_game_over_screen()
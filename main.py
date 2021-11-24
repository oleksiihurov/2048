# Project imports
import config as c
from game import Game
from graphics import *


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_move_done = False
        self.game = Game(c.GRID.COLS, c.GRID.ROWS)

    def loop_handler(self):
        """Resetting flags. Ticking internal clock by FPS."""
        self.is_move_done = False
        return self.is_running

    def events_handler(self):
        """Reacting to the events from mouse/keyboard or window manipulation."""
        for event in pg.event.get():

            # events from main window
            if event.type == pg.QUIT:
                self.is_running = False

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
                if event.key == pg.K_UP:
                    self.is_move_done = self.game.up()
                if event.key == pg.K_DOWN:
                    self.is_move_done = self.game.down()
                if event.key == pg.K_RIGHT:
                    self.is_move_done = self.game.right()
                if event.key == pg.K_LEFT:
                    self.is_move_done = self.game.left()

    def actions_handler(self):
        """Program actions in the main loop."""

        # self.is_move_done = {
        #     0: self.game.up,
        #     1: self.game.down,
        #     2: self.game.right,
        #     3: self.game.left,
        # }.get(np.random.randint(4))()

        if self.is_move_done:
            self.game.generate_tile(self.game.choose_tile())
        if self.game.is_game_lost():
            from pprint import pprint
            print('Game lost!')
            print()
            print(self.game.matrix)
            print()
            print(f'{self.game.stats.score = }')
            print()
            print(f'{self.game.stats.moves_idle = }')
            print()
            pprint(self.game.stats.move)
            print()
            print(f'Total moves = {sum(self.game.stats.move.values()) + self.game.stats.moves_idle}')
            print()
            pprint(self.game.stats.merge)
            self.is_running = False

    def graphics_handler(self):
        """Redrawing the screen."""
        graphics.draw_grid(self.game.matrix)
        graphics.show()


# --- Main Program ------------------------------------------------------------

def main():
    demo = Demo()
    while demo.loop_handler():
        demo.events_handler()
        demo.actions_handler()
        demo.graphics_handler()


if __name__ == '__main__':
    main()

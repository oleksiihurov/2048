# External imports
import numpy as np
import pygame as pg
import pygame_gui as pgui

# Project imports
from config import GAME, SCREEN, ANIMATION, MOVE
from game import Game
from graphics import Graphics
from gui import GUI
from animation import Animation


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_mousemotion = False  # flag of the mouse pointer movement event
        self.move = MOVE.NONE

        # Setup graphics
        self.game = Game(GAME)
        self.graphics = Graphics(SCREEN.RESOLUTION)
        self.gui = GUI(self.graphics.screen)
        self.animation = Animation()

    def loop_handler(self):
        """Resetting flags. Ticking internal clock by FPS."""
        self.is_mousemotion = False
        self.move = MOVE.NONE
        self.graphics.clock_tick()
        return self.is_running

    def events_handler(self):
        """Reacting to the events from mouse/keyboard or window manipulation."""
        for event in pg.event.get():

            # events from main window
            if event.type == pg.QUIT:
                self.is_running = False
                break

            # events from mouse
            if event.type == pg.MOUSEMOTION:
                self.is_mousemotion = True

            # events from keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_running = False
                if event.key == pg.K_UP:
                    self.move = self.game.up()
                if event.key == pg.K_DOWN:
                    self.move = self.game.down()
                if event.key == pg.K_RIGHT:
                    self.move = self.game.right()
                if event.key == pg.K_LEFT:
                    self.move = self.game.left()
                if event.key == pg.K_BACKSPACE:
                    self.game.pop_from_history()
                    self.gui.update_score(self.game.stats.score)
                    if not self.game.is_history_there():
                        self.gui.button_undo.hide()

            # events from GUI
            if event.type == pg.USEREVENT:
                if event.user_type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gui.button_new_game:
                        self.game.new_game()
                        self.gui.update_score(self.game.stats.score)
                        self.gui.button_undo.hide()
                    if event.ui_element == self.gui.button_undo:
                        self.game.pop_from_history()
                        self.gui.update_score(self.game.stats.score)
                        if not self.game.is_history_there():
                            self.gui.button_undo.hide()

            self.gui.manager.process_events(event)
        self.gui.manager.update(self.graphics.time_delta)

    def actions_handler(self):
        """Program actions in the main loop."""

        # self.move = {
        #     0: self.game.up,
        #     1: self.game.down,
        #     2: self.game.right,
        #     3: self.game.left,
        # }.get(np.random.randint(4))()

        if self.move is not MOVE.NONE:
            self.gui.update_score(self.game.stats.score)
            self.game.generate_new_tile(self.game.choose_tile())
            if ANIMATION.IS_PRESENT:
                self.animation.start(self.game.tiles, self.move)
            if GAME.UNDO:
                self.gui.button_undo.show()
        else:
            if ANIMATION.IS_PRESENT:
                self.animation.next()

        if self.game.is_game_lost():
            self.game.game_lost_procedure()
            self.is_running = False

    def graphics_handler(self):
        """Redrawing the screen."""
        self.gui.draw()
        if ANIMATION.IS_PRESENT:
            self.graphics.animate_tiles(self.animation.tiles)
        else:
            self.graphics.draw_grid(self.game.matrix)
        self.graphics.show()

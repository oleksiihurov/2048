# -----------------------------------------------------------------------------
# "2048" tribute to original https://2048game.com
# Copyright (c) Dec 2021 Oleksii Hurov
# -----------------------------------------------------------------------------

"""
(V) Control level abstraction.
Main program. Entry point.
"""


# External imports
import numpy as np
import pygame as pg
import pygame_gui as pgui

# Project imports
from config import GAME, PANEL, SCREEN, ANIMATION, MOVE
from logic import Logic
from graphics import Graphics
from gui import GUI


# --- Demo --------------------------------------------------------------------

class Demo:

    def __init__(self):

        # Setup process
        self.is_running = True  # running main program flag
        self.is_mousemotion = False  # flag of the mouse pointer movement event
        self.move = MOVE.NONE

        # Setup graphics
        self.logic = Logic(GAME)
        self.graphics = Graphics(SCREEN.RESOLUTION)
        self.gui = GUI(self.graphics.screen)

    # --- Handle methods ------------------------------------------------------

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
                    self.move = self.logic.up()
                if event.key == pg.K_DOWN:
                    self.move = self.logic.down()
                if event.key == pg.K_RIGHT:
                    self.move = self.logic.right()
                if event.key == pg.K_LEFT:
                    self.move = self.logic.left()
                if event.key == pg.K_BACKSPACE:
                    self._event_undo()

            # events from GUI
            if event.type == pg.USEREVENT:
                if event.user_type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.gui.button_new_game:
                        self._event_new_game()
                    if event.ui_element == self.gui.button_undo:
                        self._event_undo()

            self.gui.manager.process_events(event)
        self.gui.manager.update(self.graphics.time_delta)

    def actions_handler(self):
        """Program actions in the main loop."""

        # self.move = {
        #     0: self.logic.up,
        #     1: self.logic.down,
        #     2: self.logic.right,
        #     3: self.logic.left,
        # }.get(np.random.randint(4))()

        if self.move is not MOVE.NONE:
            if PANEL.IS_PRESENT:
                self.gui.update_score(self.logic.stats.score)
            self.logic.generate_new_tile(self.logic.choose_tile())
            if ANIMATION.IS_PRESENT:
                self.logic.tiles.start_animation()
            if PANEL.IS_PRESENT and GAME.UNDO:
                self.gui.button_undo.show()
        else:
            if ANIMATION.IS_PRESENT:
                self.logic.tiles.next_animation()

        if self.logic.is_game_lost():
            self.logic.game_lost_procedure()
            self.is_running = False

    def graphics_handler(self):
        """Redrawing the screen."""
        self.gui.draw()
        if ANIMATION.IS_PRESENT:
            self.graphics.animate_tiles(self.logic.tiles)
        else:
            self.graphics.draw_grid(self.logic.matrix)
        self.graphics.show()

    # --- Other methods -------------------------------------------------------

    def _event_undo(self):
        self.logic.pop_from_history()
        if PANEL.IS_PRESENT:
            self.gui.update_score(self.logic.stats.score)
            if not self.logic.is_history_there():
                self.gui.button_undo.hide()

    def _event_new_game(self):
        self.logic.new_game()
        if PANEL.IS_PRESENT:
            self.gui.update_score(self.logic.stats.score)
            self.gui.button_undo.hide()

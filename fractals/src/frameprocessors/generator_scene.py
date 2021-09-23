import logging
from typing import List, TYPE_CHECKING

import pygame.draw
from pygame import Surface
from pygame.event import Event

from fractals.src.interfaces.scene import Scene
from fractals.src.state.game_state import GameState

if TYPE_CHECKING:
    from fractals.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = (255, 255, 255)
BOX_COLOR = "black"


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        self.log = logging.getLogger(self.__class__.__name__)

    def process_input(self, events: List[Event]):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Boxes
        box_width = screen.get_width() // 3
        box_height = screen.get_height() // 3

        # Vertical lines
        pygame.draw.line(screen, BOX_COLOR, [box_width, 0], [box_width, screen.get_height()])
        pygame.draw.line(screen, BOX_COLOR, [box_width * 2, 0], [box_width * 2, screen.get_height()])
        # Horizontal lines
        pygame.draw.line(screen, BOX_COLOR, [0, box_height], [screen.get_width(), box_height])
        pygame.draw.line(screen, BOX_COLOR, [0, box_height * 2], [screen.get_width(), box_height * 2])

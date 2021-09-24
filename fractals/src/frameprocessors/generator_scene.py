import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, TYPE_CHECKING

import pygame.draw
from pygame import Surface
from pygame.event import Event

from fractals.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from fractals.src.interfaces.scene import Scene
from fractals.src.state.game_state import GameState
from fractals.src.util.fractal import Fractal

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

        # Boxes
        self.box_width = GAME_WIDTH_PX // 3
        self.box_height = GAME_HEIGHT_PX // 3

        self.executor_pool = ThreadPoolExecutor(9)
        self.fractals = []
        self.fractal_images = []
        self.fractal_image_generation_futures = []
        for i in range(9):
            fractal = Fractal()
            fractal_image = Surface((self.box_width, self.box_height), pygame.SRCALPHA, 32)
            self.fractals.append(fractal)
            self.fractal_images.append(fractal_image)

            self.fractal_image_generation_futures.append(self.executor_pool.submit(
                fractal.calculate_image, fractal_image
            ))

        self.log = logging.getLogger(self.__class__.__name__)

    def process_input(self, events: List[Event]):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Vertical lines
        pygame.draw.line(screen, BOX_COLOR, [self.box_width, 0], [self.box_width, screen.get_height()])
        pygame.draw.line(screen, BOX_COLOR, [self.box_width * 2, 0], [self.box_width * 2, screen.get_height()])
        # Horizontal lines
        pygame.draw.line(screen, BOX_COLOR, [0, self.box_height], [screen.get_width(), self.box_height])
        pygame.draw.line(screen, BOX_COLOR, [0, self.box_height * 2], [screen.get_width(), self.box_height * 2])

        for i in range(9):
            if not self.fractal_image_generation_futures[i].done():
                continue

            fractal_image = self.fractal_images[i]
            x_pos = (i % 3) * self.box_width
            y_pos = (i % 3) * self.box_height

            screen.blit(fractal_image, (x_pos, y_pos))

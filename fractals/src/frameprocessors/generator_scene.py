import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, TYPE_CHECKING

import pygame.draw
from pygame import Surface
from pygame.event import Event

from fractals.src.constants.fractal_constants import FRACTAL_BACKGROUND_COLOR
from fractals.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from fractals.src.interfaces.scene import Scene
from fractals.src.state.game_state import GameState
from fractals.src.util.clifford_fractal import CliffordFractal
from fractals.src.util.fractal import Fractal

if TYPE_CHECKING:
    from fractals.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = FRACTAL_BACKGROUND_COLOR
BOX_OUTLINE_COLOR = "white"
BOX_BORDER = 2


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        # Boxes
        self.box_width = GAME_WIDTH_PX // 3
        self.box_height = GAME_HEIGHT_PX // 3
        self.hover_box_index = None
        self.box_rectangles = []
        for i in range(9):
            x_pos = (i % 3) * self.box_width
            y_pos = ((i // 3) % 3) * self.box_height

            self.box_rectangles.append(
                pygame.Rect(
                    x_pos + BOX_BORDER, y_pos + BOX_BORDER, self.box_width - BOX_BORDER, self.box_height - BOX_BORDER
                )
            )

        self.executor_pool = ThreadPoolExecutor(9)
        self.fractals: List[Fractal] = []
        self.fractal_images = []
        self.fractal_image_generation_futures = []

        self.log = logging.getLogger(self.__class__.__name__)

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Mouse seems to be off by a little bit so offset it
        mouse_x_abs = mouse_pos[0] - 1
        mouse_y_abs = mouse_pos[1] - 1

        # Hover
        self.hover_box_index = None
        for i in range(len(self.box_rectangles)):
            box_rectangle = self.box_rectangles[i]
            if box_rectangle.collidepoint(mouse_x_abs, mouse_y_abs):
                self.hover_box_index = i
                break

        # Process the events
        for event in events:
            # Left mouse button released
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                if self.hover_box_index is not None:
                    self._new_generation(self.hover_box_index)

    def _new_generation(self, seed_index: int):
        seed_fractal = self.fractals[seed_index]
        self.fractals[4] = seed_fractal
        self.fractal_images[4] = self.fractal_images[seed_index]
        self.fractal_image_generation_futures[4] = self.fractal_image_generation_futures[seed_index]

        for i in range(9):
            if i == 4:
                continue

            fractal = seed_fractal.mutate()
            fractal_image = Surface((self.box_width, self.box_height), pygame.SRCALPHA, 32)
            self.fractals[i] = fractal
            self.fractal_images[i] = fractal_image
            self.fractal_image_generation_futures[i] = self.executor_pool.submit(fractal.calculate_image, fractal_image)

    def update(self, time_delta: float):
        if len(self.fractals) == 0:
            for i in range(9):
                fractal = CliffordFractal()
                fractal_image = Surface((self.box_width, self.box_height), pygame.SRCALPHA, 32)
                self.fractals.append(fractal)
                self.fractal_images.append(fractal_image)

                self.fractal_image_generation_futures.append(
                    self.executor_pool.submit(fractal.calculate_image, fractal_image)
                )

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Vertical lines
        pygame.draw.line(screen, BOX_OUTLINE_COLOR, [self.box_width, 0], [self.box_width, screen.get_height()])
        pygame.draw.line(screen, BOX_OUTLINE_COLOR, [self.box_width * 2, 0], [self.box_width * 2, screen.get_height()])
        # Horizontal lines
        pygame.draw.line(screen, BOX_OUTLINE_COLOR, [0, self.box_height], [screen.get_width(), self.box_height])
        pygame.draw.line(screen, BOX_OUTLINE_COLOR, [0, self.box_height * 2], [screen.get_width(), self.box_height * 2])

        for i in range(len(self.fractal_image_generation_futures)):
            if self.fractal_image_generation_futures[i].done():
                fractal_image = self.fractal_images[i]
                screen.blit(fractal_image, (self.box_rectangles[i].x, self.box_rectangles[i].y))

            if (self.hover_box_index is not None) and (self.hover_box_index == i):
                pygame.draw.rect(screen, "yellow", self.box_rectangles[i], width=1)

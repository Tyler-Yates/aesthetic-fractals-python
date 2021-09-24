import logging

import pygame
from pygame import Surface

from fractals.src.util.expressions import _generate_dynamic_x_expression, _generate_dynamic_y_expression
from fractals.src.util.fractal import Fractal

DRAW_ITERATIONS = 500000
MAX_ALPHA = 255
ALPHA_STEP = 1
SCALE = 100


class DynamicFractal(Fractal):
    def __init__(self):
        self.x_expression = _generate_dynamic_x_expression()
        self.y_expression = _generate_dynamic_y_expression()

        self.log = logging.getLogger(self.__class__.__name__)

    def calculate_image(self, surface: Surface):
        self.log.info("Starting generation...")

        point_to_alpha = self._calculate_points(surface.get_width(), surface.get_height())

        for point, alpha in point_to_alpha.items():
            pygame.draw.line(surface, [0, 0, 0, alpha], point, point)
        self.log.info("Done!")

    def _calculate_points(self, width: int, height: int) -> dict:
        point_to_alpha = dict()

        x = 0.0
        y = 0.0
        for i in range(DRAW_ITERATIONS):
            new_x = self.x_expression.evaluate(x, y)
            new_y = self.y_expression.evaluate(x, y)
            x = new_x
            y = new_y

            # Scale the coordinates and adjust so that the center of the surface is coordinate (0,0)
            draw_x = int(round(x * SCALE + (width / 2)))
            draw_y = int(round(y * SCALE + (height / 2)))

            point = (draw_x, draw_y)
            point_alpha = point_to_alpha.get(point, 0)
            new_point_alpha = min(MAX_ALPHA, point_alpha + ALPHA_STEP)
            point_to_alpha[point] = new_point_alpha

        return point_to_alpha

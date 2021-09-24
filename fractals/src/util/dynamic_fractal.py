import logging

import pygame
from pygame import Surface

from fractals.src.constants.fractal_constants import (
    FRACTAL_DRAW_ITERATIONS,
    FRACTAL_SCALE,
    FRACTAL_MAX_ALPHA,
    FRACTAL_ALPHA_STEP,
    FRACTAL_COLOR_R,
    FRACTAL_COLOR_G,
    FRACTAL_COLOR_B,
)
from fractals.src.util.expressions import _generate_dynamic_x_expression, _generate_dynamic_y_expression
from fractals.src.util.fractal import Fractal


class DynamicFractal(Fractal):
    def __init__(self):
        self.x_expression = _generate_dynamic_x_expression()
        self.y_expression = _generate_dynamic_y_expression()

        self.log = logging.getLogger(self.__class__.__name__)

    def calculate_image(self, surface: Surface):
        self.log.info("Starting generation...")

        point_to_alpha = self._calculate_points(surface.get_width(), surface.get_height())

        for point, alpha in point_to_alpha.items():
            pygame.draw.line(surface, [FRACTAL_COLOR_R, FRACTAL_COLOR_G, FRACTAL_COLOR_B, alpha], point, point)
        self.log.info("Done!")

    def _calculate_points(self, width: int, height: int) -> dict:
        point_to_alpha = dict()

        x = 0.0
        y = 0.0
        for i in range(FRACTAL_DRAW_ITERATIONS):
            new_x = self.x_expression.evaluate(x, y)
            new_y = self.y_expression.evaluate(x, y)
            x = new_x
            y = new_y

            # Scale the coordinates and adjust so that the center of the surface is coordinate (0,0)
            draw_x = int(round(x * FRACTAL_SCALE + (width / 2)))
            draw_y = int(round(y * FRACTAL_SCALE + (height / 2)))

            point = (draw_x, draw_y)
            point_alpha = point_to_alpha.get(point, 0)
            new_point_alpha = min(FRACTAL_MAX_ALPHA, point_alpha + FRACTAL_ALPHA_STEP)
            point_to_alpha[point] = new_point_alpha

        return point_to_alpha

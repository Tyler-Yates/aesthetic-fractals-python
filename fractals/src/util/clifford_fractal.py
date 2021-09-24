import logging
import random

import numpy
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
from fractals.src.util.clifford_expression import clifford_expression
from fractals.src.util.fractal import Fractal


class CliffordFractal(Fractal):
    def __init__(self, a: float = None, b: float = None, c: float = None, d: float = None):
        self.a = a if a else random.uniform(-2.0, 2.0)
        self.b = b if b else random.uniform(-2.0, 2.0)
        self.c = c if c else random.uniform(-2.0, 2.0)
        self.d = d if d else random.uniform(-2.0, 2.0)

        self.log = logging.getLogger(self.__class__.__name__)

    def _calculate_points(self):
        point_to_alpha = dict()

        self.log.info("Starting generation...")

        x = 0
        y = 0
        for i in range(FRACTAL_DRAW_ITERATIONS):
            x, y = clifford_expression(x, y, self.a, self.b, self.c, self.d)
            # Scale the coordinates and adjust so that the center of the surface is coordinate (0,0)
            draw_x = int(round(x * FRACTAL_SCALE + 100))
            draw_y = int(round(y * FRACTAL_SCALE + 100))

            point = (draw_x, draw_y)
            point_alpha = point_to_alpha.get(point, 0)
            new_point_alpha = min(FRACTAL_MAX_ALPHA, point_alpha + FRACTAL_ALPHA_STEP)
            point_to_alpha[point] = new_point_alpha

        self.log.info("Finished generation")

        return point_to_alpha

    def calculate_image(self, surface: Surface):
        point_to_alpha = self._calculate_points()

        for point, alpha in point_to_alpha.items():
            pygame.draw.line(surface, [FRACTAL_COLOR_R, FRACTAL_COLOR_G, FRACTAL_COLOR_B, alpha], point, point)

    def mutate(self) -> "CliffordFractal":
        new_a = self.a + numpy.random.normal(loc=0.0, scale=0.1)
        new_b = self.b + numpy.random.normal(loc=0.0, scale=0.1)
        new_c = self.c + numpy.random.normal(loc=0.0, scale=0.1)
        new_d = self.d + numpy.random.normal(loc=0.0, scale=0.1)

        return CliffordFractal(new_a, new_b, new_c, new_d)

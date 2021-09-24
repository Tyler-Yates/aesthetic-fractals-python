from abc import ABC

from pygame import Surface


class Fractal(ABC):
    def calculate_image(self, surface: Surface):
        raise NotImplementedError("Subclass must implement.")

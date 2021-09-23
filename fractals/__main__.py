import logging

import pygame

from fractals.src.controllers.controller import Controller
from fractals.src.frameprocessors.performance_overlay import PerformanceOverlay
from fractals.src.constants.game_constants import GAME_NAME, GAME_FPS, GAME_WIDTH_PX, GAME_HEIGHT_PX
from fractals.src.controllers.scene_controller import SceneController
from fractals.src.state.game_state import GameState

logging.basicConfig(level=logging.INFO)


def main():
    game_state = GameState()
    scene_controller = SceneController(game_state)

    overlays = [PerformanceOverlay(game_state, scene_controller)]

    director = Controller(GAME_NAME, game_state, scene_controller, GAME_FPS, GAME_WIDTH_PX, GAME_HEIGHT_PX, overlays)
    director.loop()


if __name__ == "__main__":
    pygame.init()
    main()

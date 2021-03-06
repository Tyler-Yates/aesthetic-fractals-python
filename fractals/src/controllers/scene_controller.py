from fractals.src.constants.scene_enum import SceneEnum
from fractals.src.frameprocessors.generator_scene import GameScene
from fractals.src.frameprocessors.main_menu_scene import MainMenuScene
from fractals.src.interfaces.scene import Scene
from fractals.src.state.game_state import GameState


class SceneController:
    """
    Class to manage the active scene of the game.
    """

    def __init__(self, game_state: GameState):
        self.game_state = game_state

        # Default to Main Menu
        self.active_scene: Scene = self._get_scene_object(SceneEnum.MainMenu)

    def _get_scene_object(self, scene_id: SceneEnum) -> Scene:
        if scene_id == SceneEnum.MainMenu:
            return MainMenuScene(self.game_state, self)
        if scene_id == SceneEnum.Generator:
            return GameScene(self.game_state, self)

    def get_active_scene(self) -> Scene:
        return self.active_scene

    def change_active_scene(self, next_scene: SceneEnum):
        self.active_scene = self._get_scene_object(next_scene)

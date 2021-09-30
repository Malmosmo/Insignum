import config
from util.util import loadImage
from gsm import State


class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        # self.map = MapHandler( MAP_NAME )
        # self.player ...

        self.background = loadImage(config.textures / "background2")

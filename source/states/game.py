import pygame
import config
from util.util import loadImage
from gsm import State


class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        # self.map = MapHandler( MAP_NAME )
        # self.player ...

        self.background = loadImage(config.textures / "background2.jpg")

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.exitState()

    def update(self, dt):
        pass

    def render(self, screen):
        screen.blit(self.background, (0, 0))

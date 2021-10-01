import config
import pygame

from gsm import State
from handler import MapHandler
from player import Player
from handler import CollisionHandler
from util import loadImage


class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.map = MapHandler("test")
        self.player = Player(100, 100)

        self.collision = CollisionHandler(self.player, self.map)

        self.background = loadImage(config.textures / "background2.jpg")

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.exitState()

        self.player.event(events)

    def update(self, dt):
        self.player.update(dt)

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        self.map.render(screen)
        self.player.render(screen)

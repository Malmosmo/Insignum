import numpy as np
import config
import pygame

from gsm import State
from handler import MapHandler
from player import Player
from handler import CollisionHandler
from util import scale
from util.vector import Vec2
from util import loadImage


class GameState(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.map = MapHandler("test")
        self.player = Player(*self.map.start)

        self.collision = CollisionHandler(self.player, self.map)

        self.background = scale(loadImage(config.textures / "background2.jpg"), 0.5)

        self.offset = Vec2(0, 0)
        self.screenOffset = Vec2(config.width // 2, config.height // 2)

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.exitState()

        self.player.event(events)

    def update(self, dt):
        self.player.update(dt)
        self.collision.update(dt)

        # self.offset = self.player.pos.copy()
        # self.offset.x -= self.
        # self.offset.y -= 180

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        # performance ?
        self.offset += np.asarray((self.player.pos - self.screenOffset - self.offset) / 10, dtype=np.int32).view(Vec2)

        self.map.render(screen, self.offset)
        self.player.render(screen, self.offset)

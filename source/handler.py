import json
import pygame

import config
from util import loadImage


class MapHandler:
    def __init__(self, name=None) -> None:
        if name:
            self.load(name)

    def load(self, name):
        path = config.maps / name

        with open(path / "config.json", "r") as file:
            mapFile = json.load(file)

        self.tileMap = mapFile["data"]
        self.textures = {key: loadImage(path / "textures" / value) for texture in mapFile["textures"] for key, value in texture.items()}

        self.tileSize = self.textures["1"].get_width()

        self.tiles = []

        self.scrollX = 0
        self.scrollY = 0

        self.intScrollX = 0
        self.intScrollY = 0

    def event(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        self.tiles = []

        for y, row in enumerate(self.tileMap):
            for x, tile in enumerate(row):
                if tile in self.textures:
                    screen.blit(self.textures[tile], (x * self.tileSize, y * self.tileSize))

                    self.tiles.append(pygame.Rect(x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))


class CollisionHandler:
    def __init__(self, player, map_) -> None:
        self.player = player
        self.map = map_

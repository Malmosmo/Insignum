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

        self.start = mapFile["start"]
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

    def render(self, screen, offset):
        self.tiles = []

        for y, row in enumerate(self.tileMap):
            for x, tile in enumerate(row):
                if tile in self.textures:
                    screen.blit(self.textures[tile], (x * self.tileSize - offset.x, y * self.tileSize - offset.y))

                    self.tiles.append(pygame.Rect(x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))


class CollisionHandler:
    def __init__(self, player, map_) -> None:
        self.player = player
        self.map = map_

    def tileCollision(self, rect, tiles):
        hitList = []

        for tile in tiles:
            if rect.colliderect(tile):
                hitList.append(tile)

        return hitList

    def collisions(self):
        collisionTypes = {
            "top": False,
            "bottom": False,
            "right": False,
            "left": False
        }

        hitbox = self.player.getHitbox()
        velocity = self.player.velocity

        # X-axis
        hitbox.x += velocity.x
        hitList = self.tileCollision(hitbox, self.map.tiles)

        for tile in hitList:
            # moving right
            if velocity.x > 0:
                hitbox.right = tile.left
                collisionTypes["right"] = True

            # moving left
            elif velocity.x < 0:
                hitbox.left = tile.right
                collisionTypes["left"] = True

        # Y-axis
        hitbox.y += velocity.y
        hitList = self.tileCollision(hitbox, self.map.tiles)

        for tile in hitList:
            # moving bottom
            if velocity.y > 0:
                hitbox.bottom = tile.top
                collisionTypes["bottom"] = True

            # moving top
            if velocity.y < 0:
                hitbox.top = tile.bottom
                collisionTypes["top"] = True

        self.player.move(hitbox, collisionTypes)

    def update(self, dt):
        self.collisions()

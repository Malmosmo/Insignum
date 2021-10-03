import json
import pygame

import config
from util import loadImage


class SpriteSheet:
    def __init__(self, path) -> None:
        self.sprite = loadImage(path)

    def getSprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))

        sprite.blit(self.sprite, (0, 0), (x, y, w, h))

        sprite.set_colorkey((0, 0, 0))

        return sprite

    def getWidth(self):
        return self.spriteSheet.get_width()

    def getHeight(self):
        return self.spriteSheet.get_height()


class Animation:
    def __init__(self, path) -> None:
        self.flip = False
        self.animations = {}

        with open(path / "config.json", "r") as file:
            self.cfg = json.load(file)

        self.sprite = SpriteSheet(path / self.cfg["path"])
        self.width, self.height = self.cfg["size"]

        self.loadSprites()
        self.setState(self.cfg["inital"])

    def loadImages(self, imageList):
        w = self.cfg["ImageSize"][0]
        h = self.cfg["ImageSize"][1]

        images = []

        for imgNum in imageList:
            x = imgNum % self.width
            y = imgNum // self.width

            img = self.sprite.getSprite(x * w, y * h, w, h)
            images.append(img)

        return images

    def loadSprites(self):
        for animation in self.cfg["animation"]:
            images = self.loadImages(animation["images"])

            self.animations[animation["name"]] = {
                "images": images,
                "length": len(images),
                "speed": animation["speed"],
                "next": animation["next"]
            }

    def setState(self, state):
        self.state = state
        self.speed = self.animations[state]["speed"]
        self.idx = 0
        self.ctr = 0

    def changeState(self, stateName):
        if self.state != stateName:
            self.speed = self.animations[stateName]["speed"]
            self.state = stateName
            self.idx = 0
            self.ctr = 0

    def render(self, screen, x, y, motion):
        if motion["left"]:
            if not motion["top"]:
                self.changeState("running")

            self.flip = True

        elif motion["right"]:
            if not motion["top"]:
                self.changeState("running")

            self.flip = False

        if not motion["left"] and not motion["right"] and not motion["top"]:
            self.changeState("idle")

        if motion["top"] and self.state != "fall":
            self.changeState("jumping")

        elif motion["down"]:
            pass

        if self.ctr >= self.speed:
            self.ctr = 0
            self.idx += 1
            if self.idx >= self.animations[self.state]["length"]:
                self.idx = 0
                self.changeState(self.animations[self.state]["next"])

        self.ctr += 1

        screen.blit(pygame.transform.flip(self.animations[self.state]["images"][self.idx], self.flip, False), (x, y))

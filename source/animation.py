import json
from numpy.core.fromnumeric import swapaxes
import pygame

import config
from util import loadImage, renderText


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

        self.offset = self.cfg["offset"]
        self.playerSize = self.cfg["PlayerSize"]
        self.hitbox = pygame.Rect(*self.offset, *self.playerSize)

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
                "next": animation["next"],
                "interrupts": animation["interrupt"]
            }

    def setState(self, state):
        self.state = state
        self.speed = self.animations[state]["speed"]
        self.idx = 0
        self.ctr = 0

    def changeState(self, newState):
        if self.state != newState:
            # if newState in self.animations[self.state]["interrupts"]:
            self.speed = self.animations[newState]["speed"]
            self.state = newState
            self.idx = 0
            self.ctr = 0

    def render(self, screen, x, y, motion, collision):
        if motion["left"] and not motion["jump"]:
            self.changeState("run")
            self.flip = True

        if motion["right"] and not motion["jump"]:
            self.changeState("run")
            self.flip = False

        if motion["jump"] and self.state != "fall":
            self.changeState("jump")

        # if self.state == "fall" and collision["bottom"]:
        #     self.changeState("idle")

        # else:
        #     self.changeState("idle")

        # if collision["bottom"]:
        #     self.changeState("idle")

        if not (motion["left"] or motion["right"] or motion["jump"]):
            self.changeState("idle")

        if self.ctr >= self.speed:
            self.ctr = 0
            self.idx += 1

        if self.idx >= self.animations[self.state]["length"]:
            self.idx = 0

            if self.state == "jump":
                self.changeState("fall")

                # print(self.state, "-->", self.animations[self.state]["next"])
                # self.changeState(self.animations[self.state]["next"])

        self.ctr += 1

        # renderText(screen, str(motion), (226, 46, 21), 100, 100, pygame.font.Font(None, 20))

        screen.blit(pygame.transform.flip(self.animations[self.state]["images"][self.idx], self.flip, False), (x, y))

        # pygame.draw.rect(screen, (0, 255, 125), self.hitbox.move(x, y), True)

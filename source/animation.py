import json
import pygame

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

        self.animFrame = 0
        self.frameCounter = 0

        self.images = []
        self.length = 0
        self.speed = 0

        # Load config
        with open(path / "config.json", "r") as file:
            self.cfg = json.load(file)

        self.sprite = SpriteSheet(path / self.cfg["path"])
        self.width, self.height = self.cfg["size"]

        self.offset = self.cfg["offset"]
        self.playerSize = self.cfg["PlayerSize"]
        self.hitbox = pygame.Rect(*self.offset, *self.playerSize)

        # more setup
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
                "speed": animation["speed"]
            }

    def setState(self, state):
        self.images = self.animations[state]["images"]
        self.length = self.animations[state]["length"]
        self.speed = self.animations[state]["speed"]

        self.state = state
        self.animFrame = 0
        self.frameCounter = 0

    def changeState(self, newState):
        if self.state != newState:
            self.setState(newState)

    def render(self, screen, x, y, motion, collision):
        # Flip
        if motion["left"]:
            self.flip = True

        # elif prevents from moonwalking
        elif motion["right"]:
            self.flip = False

        # Run
        if not motion["jump"]:
            if motion["left"]:
                self.changeState("run")

            if motion["right"]:
                self.changeState("run")

        # Jump
        if motion["jump"] and self.state != "fall":
            self.changeState("jump")

        # Idle
        if not (motion["left"] or motion["right"] or motion["jump"]):
            self.changeState("idle")

        if self.frameCounter >= self.speed:
            self.frameCounter = 0
            self.animFrame += 1

        if self.animFrame >= self.animations[self.state]["length"]:
            self.animFrame = 0

            if self.state == "jump":
                self.changeState("fall")

        self.frameCounter += 1

        screen.blit(pygame.transform.flip(self.images[self.animFrame], self.flip, False), (x, y))

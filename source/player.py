import config
import pygame
from animation import Animation
from util import renderText
from util import loadImage
from util import Vec2


class Player:
    def __init__(self, x, y) -> None:
        self.pos = Vec2(x, y)
        self.velocity = Vec2(0, 9.81)

        self.movement = {
            "right": False,
            "left": False,
            "jump": False,
            "down": False,
        }

        self.coll = {}
        self.inAir = 0

        self.playerModel = loadImage(config.entities / "Player/player.png")
        self.animation = Animation(config.entities / "Player")

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.inAir < 10:
                    self.movement["jump"] = True
                    self.velocity.y = -10

                if event.key == pygame.K_a:
                    self.movement["left"] = True

                if event.key == pygame.K_d:
                    self.movement["right"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.movement["left"] = False

                if event.key == pygame.K_d:
                    self.movement["right"] = False

    def update(self, dt):
        if self.movement["left"]:
            self.velocity.x = -4

        elif self.movement["right"]:
            self.velocity.x = 4

        else:
            self.velocity.x = 0

        self.velocity.y = min(self.velocity.y + 0.5, 9.81)
        self.inAir += 1

    def render(self, screen):
        self.animation.render(screen, self.pos.x, self.pos.y, self.movement, self.collisions)

        # renderText(screen, "Colisions:" + str(self.coll), (26, 246, 121), 100, 50, pygame.font.Font(None, 20))
        # screen.blit(self.playerModel, (self.pos.x, self.pos.y))

    def getHitbox(self):
        # return self.animation.hitbox.move(*self.pos)
        return pygame.Rect(self.pos.x + 20, self.pos.y + 7, 11, 29)

    def move(self, hitbox, collisions):
        self.pos.x = hitbox.x - 20
        self.pos.y = hitbox.y - 7

        if collisions["top"]:
            self.velocity.y = 0

        if collisions["left"]:
            self.velocity.x = 0

        if collisions["right"]:
            self.velocity.x = 0

        if collisions["bottom"]:
            self.velocity.y = 0
            self.inAir = 0
            self.movement["jump"] = False

        self.collisions = collisions

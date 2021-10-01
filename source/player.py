import config
import pygame
from util import loadImage
from util import Vec2


class Player:
    def __init__(self, x, y) -> None:
        self.pos = Vec2(x, y)
        self.velocity = Vec2(0, 0)

        self.moving = {
            "right": False,
            "left": False,
            "top": False,
            "down": False,
        }

        # self.airTime = 0
        self.img = loadImage(config.entities / "Player/player.png")
        self.rect = self.img.get_rect()

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # if self.airTime < 5:
                    # self.moving["top"] = True
                    self.velocity.y = 0  # -20

                if event.key == pygame.K_a:
                    self.moving["left"] = True

                if event.key == pygame.K_d:
                    self.moving["right"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.moving["left"] = False

                if event.key == pygame.K_d:
                    self.moving["right"] = False

    def update(self, dt):
        g = 9.81 / 100

        if self.moving["left"]:
            self.velocity.x = -4

        elif self.moving["right"]:
            self.velocity.x = 4

        else:
            self.velocity.x *= 0.02

        # self.velocity.y = min(self.velocity.y + g * dt, 9)

        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        # self.airTime += 1

    def render(self, screen):
        screen.blit(self.img, (self.rect.x + self.pos.x, self.rect.y + self.pos.y))

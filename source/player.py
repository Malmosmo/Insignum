import config
import pygame
from animation import Animation
from util import renderText
from util import loadImage
from util import Vec2


class Player:
    def __init__(self, x, y) -> None:
        self.pos = Vec2(x, y)
        self.velocity = Vec2(0, 0)

        self.moving = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }

        self.coll = {}

        # self.airTime = 0
        self.playerModel = loadImage(config.entities / "Player/player.png")
        self.animation = Animation(config.entities / "Player")

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # if self.airTime < 5:
                    self.moving["up"] = True
                    self.velocity.y = 0

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
        # print(self.velocity)
        g = 9.81 / 100

        if self.moving["left"]:
            self.velocity.x = -4

        elif self.moving["right"]:
            self.velocity.x = 4

        else:
            self.velocity.x *= 0.02

        # self.velocity.y = min(self.velocity.y + g * dt, 9)
        self.velocity.y += 0.9

        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        # self.airTime += 1

    def render(self, screen):
        self.animation.render(screen, self.pos.x, self.pos.y, self.moving)

        renderText(screen, str(self.coll), (26, 246, 121), 100, 50, pygame.font.Font(None, 20))

        # screen.blit(self.img, (self.rect.x + self.pos.x, self.rect.y + self.pos.y))

    def getHitbox(self):
        return self.animation.hitbox.move(*self.pos)

    def move(self, hitbox, collisions):
        # DEBUG(hitbox)
        self.pos.x, self.pos.y = hitbox.x - self.animation.offset[0], hitbox.y - self.animation.offset[1]

        # self.animation.hitbox.x = self.x
        # self.animation.hitbox.y = self.y

        if collisions["top"]:
            self.velocity.y = 10

        if collisions["bottom"]:
            # print("STOP!")
            if self.velocity.y > 0:
                self.moving["up"] = False
                self.velocity.y = 0

            # self.airTime = 0

        self.coll = collisions


def DEBUG(*args):
    for arg in [*args]:
        print(f"""
            Type: {type(arg)},
            Value: {arg}
        """)

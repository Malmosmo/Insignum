from pathlib import Path

import pygame

import config
from gsm import GameStateManager
from states import MainMenu


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.running = True
        self.fps = 60

        self.clock = pygame.time.Clock()

        self.screenWidth = config.width
        self.screenHeight = config.height

        self.width = self.screenWidth
        self.height = self.screenHeight

        self.center = (self.width // 2, self.height // 2)

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.surface = pygame.Surface((self.width, self.height))

        self.font = pygame.font.Font(config.fonts / "hemi_head.ttf", 50)

        self.gsm = GameStateManager(self)
        self.gsm.add(MainMenu)

        self.timePassed = 1

    def event(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.gsm.event(events)

    def update(self, dt):
        self.gsm.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))

        self.gsm.render(self.screen)

        fpsImg = self.font.render(str(int(self.timePassed)), True, (0, 255, 0))
        self.screen.blit(fpsImg, (0, 0))

        pygame.display.update()

    def run(self):
        dt = 1 / self.fps

        while self.running:
            self.event()
            self.update(dt)
            self.render()

            dt = 1000 / self.clock.tick(self.fps)
            self.timePassed = dt

        pygame.quit()

    def close(self):
        self.running = False


if __name__ == "__main__":
    print("Hello!")
    Game().run()

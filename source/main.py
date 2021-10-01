import pygame

import config
from gsm import GameStateManager
from states import MainMenu


def init():
    pygame.init()
    pygame.font.init()


class Game:
    def __init__(self) -> None:
        self.running = True
        self.fps = config.FPS

        self.clock = pygame.time.Clock()

        self.width = config.width
        self.height = config.height

        self.screenWidth = self.width * config.scale
        self.screenHeight = self.height * config.scale

        self.center = (self.width // 2, self.height // 2)

        self.window = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen = pygame.Surface((self.width, self.height))

        self.font = pygame.font.Font(config.fonts / "hemi_head.ttf", 25)

        self.gsm = GameStateManager(self)
        self.gsm.add(MainMenu)

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

        fpsImg = self.font.render(str(int(self.clock.get_fps())), True, (0, 255, 0))
        self.screen.blit(fpsImg, (0, 0))

        scaledScreen = pygame.transform.scale(self.screen, (self.screenWidth, self.screenHeight))
        self.window.blit(scaledScreen, (0, 0))

        pygame.display.update()

    def run(self):
        dt = 1 / self.fps

        while self.running:
            self.event()
            self.update(dt)
            self.render()

            dt = self.clock.tick_busy_loop(self.fps)

        pygame.quit()

    def close(self):
        self.running = False


if __name__ == "__main__":
    init()
    game = Game()
    config.game = game
    game.run()

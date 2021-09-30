from states.game import GameState
import pygame
import config
from gsm import State
from util import renderImage, renderText, loadImage
from widgets import Button


class MainMenu(State):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.widgets = [
            Button(self.game.center[0], 150, "Start", lambda:self.game.gsm.add(GameState), self.game),
            Button(self.game.center[0], 300, "Quit", self.game.close, self.game),
        ]

        self.active = 0
        self.widgets[self.active].select()
        self.background = loadImage(config.textures / "background1.jpg")

    def event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.widgets[self.active].deselect()
                    self.active = max(self.active - 1, 0)
                    self.widgets[self.active].select()

                if event.key == pygame.K_s:
                    self.widgets[self.active].deselect()
                    self.active = min(self.active + 1, len(self.widgets) - 1)
                    self.widgets[self.active].select()

                if event.key == pygame.K_RETURN:
                    self.widgets[self.active].onClick()

    def render(self, screen):
        renderImage(screen, self.background, *self.game.center, True)

        for button in self.widgets:
            button.render(screen)

        renderText(screen, "INSIGNUM", (76, 86, 21), self.game.center[0], 50, self.game.font, True)

import config
from util import renderImage, renderText, loadImage, scale


class Button:
    def __init__(self, x, y, text, callback, game) -> None:
        self.game = game
        self.x = x
        self.y = y

        self.text = text
        self.callback = callback

        self.selected = False

        self.img = scale(loadImage(config.textures / "button.png"), 2)
        self.font = self.game.font

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def onClick(self):
        if self.callback:
            self.callback()

    def event(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        renderImage(screen, self.img, self.x, self.y, True)

        if self.selected:
            renderText(screen, self.text, (125, 215, 125), self.x, self.y, self.font, True)

        else:
            renderText(screen, self.text, (50, 50, 50), self.x, self.y, self.font, True)

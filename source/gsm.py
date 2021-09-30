class GameStateManager:
    def __init__(self, game) -> None:
        self.game = game
        self.stateStack = []

    def event(self, events):
        self.stateStack[-1].event(events)

    def update(self, dt):
        self.stateStack[-1].update(dt)

    def render(self, screen):
        self.stateStack[-1].render(screen)

    def add(self, stateClass):
        self.stateStack.append(stateClass(self.game))


class State:
    def __init__(self, game) -> None:
        self.game = game

        self.prevState = None

    def event(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

    def enterState(self):
        if len(self.game.gsm.stateStack) > 1:
            self.prevState = self.game.gsm.stateStack[-1]

        self.game.gsm.stateStack.append(self)

    def exitState(self):
        self.game.gsm.stateStack.pop()

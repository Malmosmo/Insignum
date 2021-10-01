import numpy as np
import math


class Vec2(np.ndarray):
    def __new__(cls, x, y):
        return np.asarray([x, y]).view(cls)

    def __array_finalize__(self, obj):
        return

    def __str__(self) -> str:
        return f"vec2({super().__str__()})"

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        return self / self.length

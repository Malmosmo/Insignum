import numpy as np
import math


class Vec2(np.ndarray):
    def __new__(cls, x=0, y=0):
        return np.asarray([x, y]).view(cls)

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

    @length.setter
    def length(self, value):
        self *= value / self.length

    @property
    def angle(self):
        return np.arctan2(self.y, self.x)

    @angle.setter
    def angle(self, value):
        pass

    def copy(self):
        return Vec2(self.x, self.y)

    def normalize(self):
        return self / self.length

    def rotate(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        R = np.array(((c, -s), (s, c)))
        return R.dot(self)

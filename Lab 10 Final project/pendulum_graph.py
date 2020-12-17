import pygame
from pygame.draw import *

from my_variables import *
from pendulum import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class PendulumGraph:
    def __init__(self, other: Pendulum):
        self._p = other

    def spring(self, x=SCREEN_X / 2, width=20, n=10):
        y = 20
        h = SCREEN_Y / 3 - self._p.h - 2 * y
        line(screen, BLACK, (x, 0), (x, 20))
        line(screen, BLACK, (x, h + 40), (x, h + 20))
        for i in range(n):
            line(screen, BLACK, (x, y), (x + width, y + h / n / 2))
            line(screen, BLACK, (x + width, y + h / n / 2), (x, y + h / n))
            y += h / n
            width = - width

    def load(self, height=5, width=SCREEN_X / 4):
        rect(
            screen,
            BLACK,
            (
                int(SCREEN_X / 2 - width),
                int(SCREEN_Y / 3 - self._p.h - height),
                int(2 * width),
                int(height)
            )
        )

    def ball(self):
        circle(
            screen,
            BLACK,
            (
                int(SCREEN_X / 2 + self._p.length * sin(self._p.a)),
                int(SCREEN_Y / 3 - self._p.h + self._p.length * cos(self._p.a))
            ),
            10
        )

    def rope(self):
        line(
            screen,
            BLACK,
            (
                SCREEN_X / 2 + self._p.length * sin(self._p.a),
                SCREEN_Y / 3 - self._p.h + self._p.length * cos(self._p.a)
            ),
            (
                SCREEN_X / 2,
                SCREEN_Y / 3 - self._p.h
            )
        )

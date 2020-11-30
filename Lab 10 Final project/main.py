from math import sin, cos

import pygame
from pygame.draw import *
import time

from my_colors import *

pygame.init()

FPS = 60
SCREEN_X, SCREEN_Y = 1300, 600
GROUND_Y = 19 * SCREEN_Y // 20

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.pendulum = Pendulum(h=0, a=0, dh=3.5, da=0.025, k=0.01, m=1, b_a=0.001, b_h=0.001)
        self.graph = PendulumGraph(self.pendulum)

    def mainloop(self):

        finished = False

        last_time = time.time()

        while not finished:
            self.pendulum.move()
            now = time.time()
            if now - last_time > 1 / FPS:
                self.graph.ball()
                self.graph.rope()
                self.graph.load()
                self.graph.spring(x=SCREEN_X / 3)
                self.graph.spring(x=2 * SCREEN_X / 3)
                last_time = time.time()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finished = True
                pygame.display.update()
                screen.fill(WHITE)


class Pendulum:
    def __init__(self, h, a, dh, da, k=0.02, l=300, m=1.0, g=0.2, b_a=0.0, b_h=0.0):
        """

        h: vertical displacement of the springs
        a: angular displacement of the pendulum
        dh: derivative of h
        da: derivative of a
        d2h: second derivative of h
        d2a: second derivative of a
        k: the spring constant divided by the mass of the ball
        l: length of the rope
        m: mass of the load divided by the mass of the ball
        g: acceleration of the free fall
        b_a: dissipation coefficient of the ball
        b_h: dissipation coefficient of the load
        """
        self.k = k
        self.l = l
        self.m = m
        self.g = g
        self.b_a = b_a
        self.b_h = b_h
        self.h = h
        self.a = a
        self.dh = dh
        self.da = da
        self.d2h = 0
        self.d2a = 0
        self.last_time = time.time()

    def move(self):
        now = time.time()
        dt, self.last_time = now - self.last_time, time.time()
        coef = 120 * dt
        self.d2h = (self.g * sin(self.a) ** 2 - self.k * self.h - self.l * cos(self.a) * self.da ** 2 - self.dh * (
                self.b_h + self.b_a * cos(self.a) ** 2)) / (cos(self.a) ** 2 + self.m)
        self.d2a = -(self.g * sin(self.a) + self.d2h * sin(self.a) + self.b_a * (
                self.dh * sin(self.a) + self.da * self.l)) / self.l
        self.dh += self.d2h * coef
        self.h += self.dh * coef
        self.da += self.d2a * coef
        self.a += self.da * coef


class PendulumGraph:
    def __init__(self, pendul):
        self._p = pendul

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
                SCREEN_X / 2 + self._p.l * sin(self._p.a),
                SCREEN_Y / 3 - self._p.h + self._p.l * cos(self._p.a)
            ),
            10
        )

    def rope(self):
        line(
            screen,
            BLACK,
            (
                SCREEN_X / 2 + self._p.l * sin(self._p.a),
                SCREEN_Y / 3 - self._p.h + self._p.l * cos(self._p.a)
            ),
            (
                SCREEN_X / 2,
                SCREEN_Y / 3 - self._p.h
            )
        )


if __name__ == "__main__":
    try:
        game = Game()
        game.mainloop()
    finally:
        pygame.quit()

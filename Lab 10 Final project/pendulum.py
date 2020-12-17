import time
from math import sin, cos, asin, pi

import pygame
from pygame.draw import *

from my_colors import *

pygame.init()

FPS = 60
SCREEN_X, SCREEN_Y = 1300, 600
GROUND_Y = 19 * SCREEN_Y // 20

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

class Pendulum:
    def __init__(self, h, a, dh, da, k=10.0, length=30.0, m=1.0, g=10.0, b_a=10.0, b_h=10.0):
        """
        h: vertical displacement of the load
        a: angular displacement of the pendulum
        dh: derivative of h
        da: derivative of a
        d2h: second derivative of h
        d2a: second derivative of a
        k: the spring constant divided by the mass of the ball
        length: length of the rope
        m: mass of the load divided by the mass of the ball
        g: acceleration of the free fall
        b_a: dissipation coefficient of the ball
        b_h: dissipation coefficient of the load
        higher: Bool, if True the ball is higher than the load
        """
        self.k = k / 1000
        self.length = length * 10
        self.m = m
        self.g = g / 50
        self.b_a = b_a / 10000
        self.b_h = b_h / 10000
        self.h = h * 10
        self.a = a / (180 / pi)
        self.dh = dh / 2
        self.da = da / 200
        self.d2h = 0
        self.d2a = 0
        self.last_time = time.time()
        self.dt = 0
        self.coefficient = 120 * self.dt
        self.higher = 0

    def time(self):
        now = time.time()
        self.dt, self.last_time = now - self.last_time, time.time()
        self.coefficient = 120 * self.dt

    def move(self):
        self.d2h = (self.g * sin(self.a) ** 2 - self.k * self.h - self.length * cos(self.a) * self.da ** 2 - self.dh * (
                self.b_h + self.b_a * cos(self.a) ** 2)) / (cos(self.a) ** 2 + self.m)
        self.d2a = -(self.g * sin(self.a) + self.d2h * sin(self.a) + self.b_a * (
                self.dh * sin(self.a) + self.da * self.length)) / self.length
        self.dh += self.d2h * self.coefficient
        self.h += self.dh * self.coefficient
        self.da += self.d2a * self.coefficient
        self.a += self.da * self.coefficient

    def mouse(self):
        x, y = pygame.mouse.get_pos()
        if y > SCREEN_Y / 3 - self.h:
            self.higher = 0
        else:
            self.higher = 1
        if x > SCREEN_X / 2 + self.length:
            self.a = pi / 2
        elif x < SCREEN_X / 2 - self.length:
            self.a = -pi / 2
        else:
            self.a = (1 - 2 * self.higher) * asin((x - SCREEN_X / 2) / self.length) + pi * self.higher

        self.h = -(y - SCREEN_Y / 3 - self.length * cos(self.a))
        self.da, self.dh = 0, 0

    def equilibrium(self):
        self.h, self.a, self.dh, self.da, self.k = 0.0, 0.0, 0.0, 0.0, 0.01
        self.m, self.g, self.length, self.b_a, self.b_h = 2.0, 0.2, 300, 0.001, 0.001

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

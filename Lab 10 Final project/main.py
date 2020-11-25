from math import sin, cos

import pygame
from pygame.draw import *

from my_colors import *

pygame.init()

FPS = 120
SCREEN_X, SCREEN_Y = 1300, 600
GROUND_Y = 19 * SCREEN_Y // 20

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))


class Pendulum:
    def __init__(self, h, a, dh, da, w=0.02, l=300, m=1, g=0.2):
        """

        h: vertical displacement of the springs
        a: angular displacement of the pendulum
        dh: derivative of h
        da: derivative of a
        d2h: second derivative of h
        d2a: second derivative of a
        w: the spring constant divided by the mass of ball
        l: length of the rope
        m: mass of the load
        g: acceleration of the free fall
        """
        self.w = w
        self.l = l
        self.m = m
        self.g = g
        self.h = h
        self.a = a
        self.dh = dh
        self.da = da
        self.d2h = 0
        self.d2a = 0

    def move(self):
        self.d2h = (self.g * sin(self.a) ** 2 - self.w * self.h - self.l * cos(self.a) * self.da ** 2) / \
                   (cos(self.a) ** 2 + self.m)
        self.d2a = -(self.g + self.d2h) * sin(self.a) / self.l
        self.dh += self.d2h
        self.h += self.dh
        self.da += self.d2a
        self.a += self.da

    def spring(self, x=SCREEN_X / 2, width=20, n=10):
        y = 20
        h = SCREEN_Y / 3 - self.h - 2 * y
        line(screen, BLACK, (x, 0), (x, 20))
        line(screen, BLACK, (x, h + 40), (x, h + 20))
        for i in range(n):
            line(screen, BLACK, (x, y), (x + width, y + h / n / 2))
            line(screen, BLACK, (x + width, y + h / n / 2), (x, y + h / n))
            y += h / n
            width = - width

    def load(self, height=5, width=SCREEN_X / 4):
        rect(screen, BLACK,
             (int(SCREEN_X / 2 - width), int(SCREEN_Y / 3 - self.h - height), int(2 * width), int(height)))

    def ball(self):
        circle(screen, BLACK, (SCREEN_X / 2 + self.l * sin(self.a), SCREEN_Y / 3 - self.h + self.l * cos(self.a)), 10)

    def rope(self):
        line(screen, BLACK, (SCREEN_X / 2 + self.l * sin(self.a), SCREEN_Y / 3 - self.h + self.l * cos(self.a)),
             (SCREEN_X / 2, SCREEN_Y / 3 - self.h))


clock = pygame.time.Clock()
finished = False

pendulum = Pendulum(h=0, a=0, dh=3, da=0.025, w=0.01, m=1)
while not finished:
    clock.tick(FPS)
    pendulum.move()
    pendulum.ball()
    pendulum.rope()
    pendulum.load()
    pendulum.spring(x=SCREEN_X / 3)
    pendulum.spring(x=2 * SCREEN_X / 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()

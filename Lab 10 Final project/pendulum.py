import time
from math import sin, cos, asin, pi

import pygame

from my_variables import *

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

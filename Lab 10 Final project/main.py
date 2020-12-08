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


class Game:
    def __init__(self):
        self.pendulum = Pendulum(h=0, a=0, dh=0, da=0, k=0.01, m=1, b_a=0.001, b_h=0.001)
        self.graph = PendulumGraph(self.pendulum)
        self.font = pygame.font.SysFont('arial', 25, True)

    def mainloop(self):
        finished = False
        last_time = time.time()

        while not finished:
            ok = True
            
            if pygame.mouse.get_pressed(5)[0]:
                self.pendulum.mouse()
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
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.pendulum.higher = 1
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        rect(screen, GREY, (450,200,400,200))
                        rect(screen, WHITE, (550,250,100,50))
                        rect(screen, WHITE, (700, 250, 100, 50))
                        while ok:
                            self.pendulum.equilibrium()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    ok = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if ((event.pos[0] - 550 < 100) and  (event.pos[0] - 550 > 0) and
                                        (event.pos[1] - 250 < 50) and (event.pos[1] - 250 > 0)):
                                        ok = False
                                        self.pendulum.m = 2
                                    elif ((event.pos[0] - 700 < 100) and  (event.pos[0] - 700 > 0) and
                                        (event.pos[1] - 250 < 50) and (event.pos[1] - 250 > 0)):
                                        ok = False
                                        self.pendulum.k = 5
                                    
                                        
                            pygame.display.update()
                            
                            



                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        self.pendulum.equilibrium()
                pygame.display.update()
                screen.fill(WHITE)


class Pendulum:
    def __init__(self, h, a, dh, da, k=0.02, length=300, m=1.0, g=0.2, b_a=0.0, b_h=0.0):
        """

        h: vertical displacement of the springs
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
        self.k = k
        self.length = length
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
        self.higher = 0

    def move(self):
        now = time.time()
        dt, self.last_time = now - self.last_time, time.time()
        coefficient = 120 * dt
        self.d2h = (self.g * sin(self.a) ** 2 - self.k * self.h - self.length * cos(self.a) * self.da ** 2 - self.dh * (
                self.b_h + self.b_a * cos(self.a) ** 2)) / (cos(self.a) ** 2 + self.m)
        self.d2a = -(self.g * sin(self.a) + self.d2h * sin(self.a) + self.b_a * (
                self.dh * sin(self.a) + self.da * self.length)) / self.length
        self.dh += self.d2h * coefficient
        self.h += self.dh * coefficient
        self.da += self.d2a * coefficient
        self.a += self.da * coefficient

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
        self.h, self.a, self.dh, self.da = 0, 0, 0, 0


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


if __name__ == "__main__":
    try:
        game = Game()
        game.mainloop()
    finally:
        pygame.quit()



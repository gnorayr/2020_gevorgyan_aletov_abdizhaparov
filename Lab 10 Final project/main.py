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


class Simulator:
    def __init__(self):
        self.pendulum = Pendulum(h=0, a=0, dh=0.0, da=0.0, k=10.0, m=2.0, b_a=10, b_h=10)
        self.graph = PendulumGraph(self.pendulum)
        self.menu = Menu(self.pendulum)

    def mainloop(self):
        finished = False
        last_time = time.time()
        menu_is_open = True

        while not finished:
            self.pendulum.time()
            if menu_is_open:
                screen.fill(GREY)
                self.menu.lil_windows()
                self.menu.text_for_lil_windows()
                self.menu.start_button_graph()
                self.menu.text()
                pygame.display.update()
            else:
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
                    pygame.display.update()
                    screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.pendulum.higher = 1
                    if menu_is_open and self.menu.start_button_check(event.pos[0], event.pos[1]):
                        menu_is_open = not menu_is_open
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        menu_is_open = not menu_is_open
                    if event.key == pygame.K_ESCAPE:
                        finished = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.pendulum.equilibrium()

            if pygame.mouse.get_pressed(3)[0]:
                if menu_is_open and self.menu.up_buttons_check(event.pos[0], event.pos[1]):
                    if self.menu.up_window_number == 1:
                        self.pendulum.h += 5 / 30
                    elif self.menu.up_window_number == 2:
                        self.pendulum.a += pi / 18 / 150
                    elif self.menu.up_window_number == 3:
                        self.pendulum.dh += 0.5 / 75
                    elif self.menu.up_window_number == 4:
                        self.pendulum.da += 0.005 / 75
                    elif self.menu.up_window_number == 5:
                        self.pendulum.k += 0.0015 / 50
                    elif self.menu.up_window_number == 6:
                        self.pendulum.length += 15 / 50
                    elif self.menu.up_window_number == 7:
                        self.pendulum.m += 0.1 / 10
                    elif self.menu.up_window_number == 8:
                        self.pendulum.g += 0.01 / 30
                    elif self.menu.up_window_number == 9:
                        self.pendulum.b_a += 0.0001 / 50
                    elif self.menu.up_window_number == 10:
                        self.pendulum.b_h += 0.0001 / 50
                    self.menu.up_window_number = 0

                if menu_is_open and self.menu.down_buttons_check(event.pos[0], event.pos[1]):
                    if self.menu.down_window_number == 1:
                        self.pendulum.h -= 5 / 30
                    elif self.menu.down_window_number == 2:
                        self.pendulum.a -= pi / 18 / 150
                    elif self.menu.down_window_number == 3:
                        self.pendulum.dh -= 0.5 / 75
                    elif self.menu.down_window_number == 4:
                        self.pendulum.da -= 0.005 / 75
                    elif self.menu.down_window_number == 5:
                        self.pendulum.k -= 0.0015 / 50
                    elif self.menu.down_window_number == 6:
                        self.pendulum.length -= 15 / 50
                    elif self.menu.down_window_number == 7:
                        self.pendulum.m -= 0.1 / 10
                    elif self.menu.down_window_number == 8:
                        self.pendulum.g -= 0.01 / 30
                    elif self.menu.down_window_number == 9:
                        self.pendulum.b_a -= 0.0001 / 50
                    elif self.menu.down_window_number == 10:
                        self.pendulum.b_h -= 0.0001 / 50
                    self.menu.down_window_number = 0


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


class Menu:
    def __init__(self, other: Pendulum):
        self.font = pygame.font.SysFont('arial', 15, True)
        self.up_window_number = 0
        self.down_window_number = 0
        self._p = other
        self.parameters_1 = [
            (self._p.h / 10, "h"),
            (self._p.a * 10, "a"),
            (self._p.dh * 2, "dh"),
            (self._p.da * 200, "da"),
            (self._p.k * 1000, "k")
        ]
        self.parameters_2 = [
            (self._p.length / 10, "length"),
            (self._p.m, "m"),
            (self._p.g * 50, "g"),
            (self._p.b_a * 10000, "b_a"),
            (self._p.b_h * 10000, "b_h")
        ]
        self.start_x = SCREEN_X / 12
        self.start_y = 3 * SCREEN_Y / 5
        self.x = self.start_x
        self.y = self.start_y
        self.side_x = 150
        self.side_y = 35

    def lil_windows(self):
        for j in range(2):
            for i in range(5):
                rect(
                    screen,
                    WHITE,
                    [
                        self.x + self.side_x / 2,
                        self.y, self.side_x, self.side_y
                    ]
                )
                line(
                    screen,
                    RED,
                    (
                        self.x + 7 * self.side_x / 10,
                        self.y + 13
                    ),
                    (
                        self.x + 13 * self.side_x / 10,
                        self.y + 13
                    )
                )
                line(
                    screen,
                    RED,
                    (
                        self.x + 7 * self.side_x / 10,
                        self.y
                    ),
                    (
                        self.x + 7 * self.side_x / 10,
                        self.y + self.side_y
                    )
                )
                line(
                    screen,
                    RED,
                    (
                        self.x + 13 * self.side_x / 10,
                        self.y
                    ),
                    (self.x + 13 * self.side_x / 10,
                     self.y + self.side_y
                     )
                )
                self.x += (SCREEN_X - 2 * self.side_x) / 5
            self.y += 2 * self.side_y
            self.x = self.start_x
        self.x = self.start_x
        self.y = self.start_y

    def text_for_lil_windows(self):
        param = self.parameters_1
        for j in range(2):
            for value, name in param:
                text_1 = self.font.render(str(round(value, 1)), True, RED)
                text_2 = self.font.render(str(name), True, RED)
                text_3 = self.font.render(">", True, RED)
                text_4 = self.font.render("<", True, RED)

                screen.blit(text_4, text_4.get_rect(center=(self.x + 6 * self.side_x / 10, self.y + self.side_y / 2)))
                screen.blit(text_3, text_3.get_rect(center=(self.x + 14 * self.side_x / 10, self.y + self.side_y / 2)))
                screen.blit(text_1, text_1.get_rect(center=(self.x + self.side_x, self.y + self.side_y / 2 + 8)))
                screen.blit(text_2, text_2.get_rect(center=(self.x + self.side_x, self.y + 5)))
                self.x += (SCREEN_X - 2 * self.side_x) / 5

            self.y += 2 * self.side_y
            self.x = self.start_x

            param = self.parameters_2

        self.x = self.start_x
        self.y = self.start_y

        self.parameters_1 = [
            (self._p.h / 10, "h"),
            (self._p.a * 180 / pi, "a"),
            (self._p.dh * 2, "dh"),
            (self._p.da * 200, "da"),
            (self._p.k * 1000, "k")
        ]
        self.parameters_2 = [
            (self._p.length / 10, "length"),
            (self._p.m, "m"),
            (self._p.g * 50, "g"),
            (self._p.b_a * 10000, "b_a"),
            (self._p.b_h * 10000, "b_h")
        ]

    def start_button_graph(self):
        font = pygame.font.SysFont('arial', 50, True)
        rect(screen, RED, [SCREEN_X / 2 - self.side_x, 8 * SCREEN_Y / 10, 2 * self.side_x, 2.5 * self.side_y])
        text_4 = font.render("START", True, WHITE)
        screen.blit(text_4, text_4.get_rect(center=(SCREEN_X / 2, 8 * SCREEN_Y / 10 + 1.25 * self.side_y)))

    def start_button_check(self, mouse_x, mouse_y):
        return 0 < mouse_x - (SCREEN_X / 2 - self.side_x) < 2 * self.side_x and \
               0 < mouse_y - (8 * SCREEN_Y / 10) < 2.5 * self.side_y

    def up_buttons_check(self, mouse_x, mouse_y):
        a = 1
        for j in range(2):
            for i in range(5):
                if 0 < mouse_x - (self.x + 13 * self.side_x / 10) < 2 * self.side_x / 10 and \
                        0 < mouse_y - self.y < self.side_y:
                    self.up_window_number = a
                a += 1
                self.x += (SCREEN_X - 2 * self.side_x) / 5
            self.y += 2 * self.side_y
            self.x = self.start_x
        self.x = self.start_x
        self.y = self.start_y

        return self.up_window_number

    def down_buttons_check(self, mouse_x, mouse_y):
        a = 1
        for j in range(2):
            for i in range(5):
                if 0 < mouse_x - (self.x + self.side_x / 2) < 2 * self.side_x / 10 and \
                        0 < mouse_y - self.y < self.side_y:
                    self.down_window_number = a
                a += 1
                self.x += (SCREEN_X - 2 * self.side_x) / 5
            self.y += 2 * self.side_y
            self.x = self.start_x
        self.x = self.start_x
        self.y = self.start_y

        return self.down_window_number

    def text(self):
        font = pygame.font.SysFont('arial', 20, True)

        text_1 = font.render("This is a simulator of a pendulum with a rope and a spring.", True, WHITE)
        text_2 = font.render(
            "You can change positions, velocities, masses, and dissipation coefficients of the ball and the load,",
            True,
            WHITE
        )
        text_3 = font.render(
            "Besides changing in menu you can change position of the ball with holding left click.",
            True,
            WHITE
        )
        text_4 = font.render(
            "You can reset variables to their defaults with right click (works both inside the menu and outside).",
            True,
            WHITE
        )
        text_15 = font.render(
            "You can enter and quit the menu by pressing TAB and you can close the simulator by pressing ESC.",
            True,
            WHITE
        )
        text_16 = font.render(
            " also you can change spring constant and the acceleration of the free fall.",
            True,
            WHITE
        )

        text_5 = font.render("h: vertical displacement of the load.", True, WHITE)
        text_6 = font.render("a: angular displacement of the pendulum (in degrees)", True, WHITE)
        text_7 = font.render("dh: derivative of h.", True, WHITE)
        text_8 = font.render("da: derivative of a.", True, WHITE)
        text_9 = font.render("k: the spring constant divided by the mass of the ball.", True, WHITE)
        text_10 = font.render("length: length of the rope.", True, WHITE)
        text_11 = font.render("m: mass of the load divided by the mass of the ball.", True, WHITE)
        text_12 = font.render("g: acceleration of the free fall.", True, WHITE)
        text_13 = font.render("b_a: dissipation coefficient of the ball.", True, WHITE)
        text_14 = font.render("b_h: dissipation coefficient of the load.", True, WHITE)

        TEXT_CENTER = [text_1, text_2, text_16, text_3, text_4, text_15]
        TEXT_LEFT = [text_5, text_6, text_7, text_8, text_9]
        TEXT_RIGHT = [text_10, text_11, text_12, text_13, text_14]

        j, k = 0, 0
        for i in range(0, 150, 25):
            screen.blit(TEXT_CENTER[j], TEXT_CENTER[j].get_rect(center=(SCREEN_X // 2, SCREEN_Y // 30 + i)))
            j += 1

        for i in range(0, 100, 20) :
            screen.blit(TEXT_LEFT[k], (SCREEN_X // 7, SCREEN_Y // 3 + i))
            screen.blit(TEXT_RIGHT[k], (4 * SCREEN_X // 7, SCREEN_Y // 3 + i))
            k += 1


if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
    finally:
        pygame.quit()

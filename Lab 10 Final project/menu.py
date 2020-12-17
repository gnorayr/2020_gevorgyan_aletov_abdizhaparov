import pygame
from pygame.draw import *

from my_variables import *
from pendulum import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

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


import time
from math import sin, cos, asin, pi

import pygame
from pygame.draw import *

from my_colors import *
from pendulum import *
from menu import *
from pendulum_graph import *
from simulator import *

pygame.init()

FPS = 60
SCREEN_X, SCREEN_Y = 1300, 600
GROUND_Y = 19 * SCREEN_Y // 20

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
    finally:
        pygame.quit()

import pygame

from my_variables import *
from pendulum import *
from menu import *
from pendulum_graph import *
from simulator import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
        
    finally:
        pygame.quit()


import pygame

from simulator import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
        
    finally:
        pygame.quit()


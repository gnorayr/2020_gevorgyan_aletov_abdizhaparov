from simulator import *

if __name__ == "__main__":
    try:
        simulator = Simulator()
        simulator.mainloop()
        
    finally:
        pygame.quit()

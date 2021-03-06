from menu import *
from pendulum_graph import *

pygame.init()


class Simulator:
    def __init__(self):
        self.pendulum = Pendulum(h=0, a=0, dh=0.0, da=0.0, k=10.0, m=2.0, b_a=10, b_h=10)
        self.graph = PendulumGraph(self.pendulum)
        self.menu = Menu(self.pendulum)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def up_button(self):
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

    def down_button(self):
        if self.menu.down_window_number == 1:
            self.pendulum.h -= 5 / 30
        elif self.menu.down_window_number == 2:
            self.pendulum.a -= pi / 18 / 150
        elif self.menu.down_window_number == 3:
            self.pendulum.dh -= 0.5 / 75
        elif self.menu.down_window_number == 4:
            self.pendulum.da -= 0.005 / 75
        elif self.menu.down_window_number == 5 and self.pendulum.k > 0.00015:
            self.pendulum.k -= 0.0015 / 50
        elif self.menu.down_window_number == 6 and self.pendulum.length > 30:
            self.pendulum.length -= 15 / 50
        elif self.menu.down_window_number == 7 and self.pendulum.m > 0.1:
            self.pendulum.m -= 0.1 / 10
        elif self.menu.down_window_number == 8 and self.pendulum.g > 0.002:
            self.pendulum.g -= 0.01 / 30
        elif self.menu.down_window_number == 9 and self.pendulum.b_a > 0.00001:
            self.pendulum.b_a -= 0.0001 / 50
        elif self.menu.down_window_number == 10 and self.pendulum.b_h > 0.00001:
            self.pendulum.b_h -= 0.0001 / 50
        self.menu.down_window_number = 0

    def mainloop(self):
        finished = False
        last_time = time.time()
        menu_is_open = True

        while not finished:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
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
                    if menu_is_open and self.menu.start_button_check(self.mouse_x, self.mouse_y):
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
                if menu_is_open and self.menu.up_buttons_check(self.mouse_x, self.mouse_y):
                    self.up_button()
                    
                if menu_is_open and self.menu.down_buttons_check(self.mouse_x, self.mouse_y):
                    self.down_button()

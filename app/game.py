import pygame
import math
import threading


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.my_font = pygame.font.SysFont('arial', 20)
        self.size = [800, 600]
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Fractals')
        self.clock = pygame.time.Clock()
        self.angle = - math.pi / 2
        self.angle_speed = 0.1
        self.lenght = 100
        self.change_len = 1.5
        self.slider = Slider(
            self.size[0] // 4, self.size[1] // 100, self.size[0] // 2, self.angle_speed, 2, 0)
        self.drag = False

    def fractal(
            self,
            length: float,
            x: int,
            y: int,
            angle: float
    ) -> None:
        if length < 1:
            pygame.draw.aaline(self.screen, (0, 0, 0), (x, y), (x +
                               length * math.cos(angle), y + length * math.sin(angle)))
        else:
            self.fractal(length / self.change_len, x + length * math.cos(angle + self.angle_speed),
                         y + length * math.sin(angle + self.angle_speed), angle + self.angle_speed)
            self.fractal(length / self.change_len, x + length * math.cos(angle - self.angle_speed),
                         y + length * math.sin(angle - self.angle_speed), angle - self.angle_speed)
            pygame.draw.aaline(self.screen, (0, 0, 0), (x, y), (x + length * math.cos(
                angle + self.angle_speed), y + length * math.sin(angle + self.angle_speed)))
            pygame.draw.aaline(self.screen, (0, 0, 0), (x, y), (x + length * math.cos(
                angle - self.angle_speed), y + length * math.sin(angle - self.angle_speed)))
        return

    def create_ui(self) -> None:
        self.slider.draw(self.screen)
        return

    def update(self) -> None:
        self.screen.fill((240, 240, 240))
        pygame.draw.aaline(self.screen,
                           (0, 0, 0),
                           (self.size[0] // 2, self.size[1]),
                           (self.size[0] // 2, self.size[1] - self.lenght))
        self.fractal(
            self.lenght, self.size[0] // 2, self.size[1] - self.lenght, self.angle)
        self.create_ui()
        pygame.display.flip()
        self.clock.tick(30)
        return

    def run(self) -> None:
        self.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.drag:
                        self.drag = True
                
                if self.drag:
                    self.angle_speed = self.slider.set_value_by_mouse_x(
                        pygame.mouse.get_pos()[0])
                    self.update()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.drag:
                        self.drag = False
        return


class Slider():
    """
    Slider for fractal animation
    """

    def __init__(
            self,
            x: int,
            y: int,
            length: int,
            value: float,
            max_value: float = 1000,
            min_value: float = 0.0,
    ) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.value = value
        self.max_value = max_value
        self.min_value = min_value

    def draw(self, window: pygame.display) -> None:
        pygame.draw.aaline(window, (0, 0, 0), (self.x, self.y),
                           (self.x + self.length, self.y))
        pygame.draw.circle(window, (0, 0, 0), (self.x + self.length /
                           (self.max_value - self.min_value) * (self.value - self.min_value), self.y), 10)
        return

    def set_value_by_mouse_x(self, mouse_pos_x: int) -> float:
        value = max(0, min(mouse_pos_x - self.x, self.length)) / \
            self.length * (self.max_value - self.min_value) + self.min_value
        self.value = min(max(value, self.min_value), self.max_value)
        return self.value
    
    def set_value(self, value: float) -> float:
        self.value = min(max(value, self.min_value), self.max_value)
        return self.value

import pygame
import math

class Map:
    def __init__(self):
        self.ascii_map = [
            "FRVVVVVVVVVV",
            "RRVVVVVVVVVV",
            "VRRVVVVVVVVV",
            "VVRRVVVVVVVV",
            "VVVRRRRRVVVV",
            "VVVVVVVRRVVV",
            "VVVVVVVVRRVV",
            "VVVVVVVVVRRV",
            "VVVVVVVVVVRS"
        ]
        self.cell_size = 50
        self.colors = {
            "V": (0, 0, 0),  # Empty cell (black)
            "R": (128, 128, 128), # Road cell (gray)
            "F": (255, 0, 0),  # Finish cell (red)
            "S": (0, 255, 0)  # Start cell (green)
        }
        self.map_width = len(self.ascii_map[0])
        self.map_height = len(self.ascii_map)
        self.window_width = self.map_width * self.cell_size
        self.window_height = self.map_height * self.cell_size

        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Map Viewer")

    def display_map(self):
        for y, line in enumerate(self.ascii_map):
            for x, cell in enumerate(line):
                pygame.draw.rect(self.window, self.colors[cell], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()

class Car:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 1
        self.deceleration = 0.5
    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)
    def accelerate(self):
        self.speed += self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def decelerate(self):
        self.speed -= self.deceleration

        if self.speed < -2:
            self.speed = -2
    def steer_left(self):
        self.direction += math.radians(5)
    def steer_right(self):
        self.direction -= math.radians(5)
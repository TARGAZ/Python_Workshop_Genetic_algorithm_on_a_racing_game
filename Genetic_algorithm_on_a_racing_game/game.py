import pygame
import math

class Map:
    def __init__(self):
        self.ascii_map = [
            "VVVVVVVVVVVVVV",
            "VSRVVVVVVVVVVV",
            "VRRVVVVVVVVVVV",
            "VVRRVVVVVVVVVV",
            "VVVRRVVVVVVVVV",
            "VVVVRRRRRVVVVV",
            "VVVVVVVVRRVVVV",
            "VVVVVVVVVRRVVV",
            "VVVVVVVVVVRRVV",
            "VVVVVVVVVVVRFV",
            "VVVVVVVVVVVVVV"
        ]
        self.cell_size = 50
        self.colors = {
            "V": (0, 0, 0),  # Empty cell (black)
            "R": (128, 128, 128), # Road cell (gray)
            "F": (0, 255, 0),  # Finish cell (green)
            "S": (255, 0, 0)  # Start cell (red)
        }
        self.map_width = len(self.ascii_map[0])
        self.map_height = len(self.ascii_map)
        self.window_width = self.map_width * self.cell_size
        self.window_height = self.map_height * self.cell_size

        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Map Viewer")

    def display_map(self):
        for y, line in enumerate(self.ascii_map):
            for x, cell in enumerate(line):
                pygame.draw.rect(self.window, self.colors[cell], (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()

class Car:
    def __init__(self):
        self.image = pygame.image.load("car.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = 50
        self.y = 50
        self.direction = 0
        self.speed = 0
        self.max_speed = 2
        self.acceleration = 1
        self.deceleration = 0.5
        self.reached_finish = False
        self.left_distance = 0
        self.right_distance = 0
        self.front_left_distance = 0
        self.front_right_distance = 0
        self.front_distance = 0
        self.radar_range = 500

    def Draw(self, game_map):
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.direction))
        self.rect = rotated_image.get_rect()
        self.rect.center = (self.x + self.width / 2, self.y + self.height / 2)  # Modifier cette ligne
        game_map.window.blit(rotated_image, self.rect)

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)

    def accelerate(self):
        self.speed += self.acceleration
        if self.speed >= self.max_speed:
            self.speed = self.max_speed

    def decelerate(self):
        self.speed -= self.deceleration
        if self.speed <= 0:
            self.speed = 0

    def steer_left(self):
        self.direction += math.radians(5)

    def steer_right(self):
        self.direction -= math.radians(5)

    def Collision(self, game_map):
        car_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for y, line in enumerate(game_map.ascii_map):
            for x, cell in enumerate(line):
                if cell != "R" and cell != "S":
                    cell_rect = pygame.Rect(x * game_map.cell_size, y * game_map.cell_size, game_map.cell_size, game_map.cell_size)
                    if car_rect.colliderect(cell_rect):
                        # Collision detected, reset car position to start
                        self.x = 50
                        self.y = 50
                        self.direction = 0
                        self.speed = 0
                if cell == "F":
                    cell_rect = pygame.Rect(x * game_map.cell_size, y * game_map.cell_size, game_map.cell_size, game_map.cell_size)
                    if car_rect.colliderect(cell_rect):
                        self.reached_finish = True
                        print("Finish reached!")

    def draw_radar_beam(self, game_map, distance, angle):
        start_x = self.x + self.width / 2
        start_y = self.y + self.height / 2
        end_x = start_x + distance * math.cos(angle)
        end_y = start_y - distance * math.sin(angle)
        pygame.draw.line(game_map.window, (255, 255, 255), (start_x, start_y), (end_x, end_y), 2)

    def radar(self, game_map):
        chosen_angle = [0, 45, 90, 315, 270]
        for angle in chosen_angle:
            angle_rad = math.radians(angle)
            for distance in range(1, self.radar_range):
                x = self.x + distance * math.cos(self.direction + angle_rad)
                y = self.y - distance * math.sin(self.direction + angle_rad)

                if x < 0 or x >= game_map.window_width or y < 0 or y >= game_map.window_height:
                    break

                cell = game_map.ascii_map[int(y / game_map.cell_size)][int(x / game_map.cell_size)]
                if cell == "V":
                    self.draw_radar_beam(game_map, distance, self.direction + angle_rad)
                    if angle == 0:
                        if distance - self.width <= 0:
                            self.front_distance = 0
                        else:
                            self.front_distance = distance - self.width
                    elif angle == 315:
                        if distance - self.width <= 0:
                            self.front_right_distance = 0
                        else:
                            self.front_right_distance = distance - self.width
                    elif angle == 270:
                        if distance - self.width <= 0:
                            self.right_distance = 0
                        else:
                            self.right_distance = distance - self.width
                    elif angle == 90:
                        if distance - self.width <= 0:
                            self.left_distance = 0
                        else:
                            self.left_distance = distance - self.width
                    elif angle == 45:
                        if distance - self.width <= 0:
                            self.front_left_distance = 0
                        else:
                            self.front_left_distance = distance - self.width
                    break


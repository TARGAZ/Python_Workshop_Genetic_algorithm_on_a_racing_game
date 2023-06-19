import pygame

class Map:
    def __init__(self):
        self.ascii_map = [
            "FRVVVVVVVVVV",
            "RRVVVVVVVVVV",
            "VRRVVVVVVVVV",
            "VVRRVVVVVVV",
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
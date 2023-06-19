import pygame
from game import *

Carte = Map()

# Main loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Carte.display_map()


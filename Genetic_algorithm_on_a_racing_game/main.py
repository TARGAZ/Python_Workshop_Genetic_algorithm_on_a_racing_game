import pygame.key

from game import *
from pygame.locals import *

Map = Map()
car = Car()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == pygame.K_UP:
                car.accelerate()
            if event.key == pygame.K_DOWN:
                car.decelerate()
            if event.key == pygame.K_LEFT:
                car.steer_left()
            if event.key == pygame.K_RIGHT:
                car.steer_right()

    car.move()
    # Efface l'écran
    Map.window.fill((255, 255, 255))

    # Affiche la carte
    Map.display_map()

    # Affiche la voiture
    pygame.draw.rect(Map.window, (0, 0, 255), (car.x, car.y, 20, 20))

    # Rafraîchit l'affichage
    pygame.display.flip()
    clock.tick(60)  # Limite le taux de rafraîchissement à 60 FPS

pygame.quit()
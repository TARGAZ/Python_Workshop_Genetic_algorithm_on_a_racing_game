import pygame.key

from game import *
from pygame.locals import *

game_map = Map()
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
            if event.key == pygame.K_ESCAPE:
                running = False

    car.move()

    # Check collision
    car.Collision(game_map)

    # Efface l'écran
    game_map.window.fill((255, 255, 255))

    # Affiche la carte
    game_map.display_map()

    # Affiche la voiture
    car.Draw(game_map)


    #radar
    car.radar(game_map)

    print("left_distance: " + str(car.left_distance))
    print("right_distance: " + str(car.right_distance))
    print("front_left_distance: " + str(car.front_left_distance))
    print("front_right_distance: " + str(car.front_right_distance))
    print("front_distance: " + str(car.front_distance))


    # Rafraîchit l'affichage
    pygame.display.flip()
    clock.tick(60)  # Limite le taux de rafraîchissement à 60 FPS

pygame.quit()
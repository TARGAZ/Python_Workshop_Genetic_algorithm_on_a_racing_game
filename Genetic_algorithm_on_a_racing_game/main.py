# Importing required modules
import pygame
import os
import neat
import time
from game import Car, Map

# Global variable to keep track of the generation
generation = 0

# Function to run the car simulation
def run_car(genomes, config):
    nets = []  # Neural networks
    cars = []  # Car objects

    # Create neural networks and car objects for each genome
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    game_map = Map()
    pygame.init()
    screen = pygame.display.set_mode((game_map.window_width, game_map.window_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 20)
    game_map.display_map()

    global generation
    generation += 1
    start_time = time.time()
    skip = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    skip = True

        if skip:
            break

        # Activate neural networks for each car and perform corresponding actions
        for x, car in enumerate(cars):
            output = nets[x].activate((car.left_distance, car.right_distance, car.front_left_distance, car.front_right_distance, car.front_distance))
            i = output.index(max(output))
            if i == 0:
                car.accelerate()
            elif i == 1:
                car.decelerate()
            elif i == 2:
                car.steer_left()
            elif i == 3:
                car.steer_right()

        game_map.window.fill((255, 255, 255))

        game_map.display_map()

        # Update car positions, check collisions, calculate distances, and draw cars
        for x, car in enumerate(cars):
            if car.nb_deaths >= 1:
                cars.pop(x)
                nets.pop(x)
                genomes.pop(x)
                break

            car.move()
            car.Collision(game_map)
            car.calculate_distances()
            car.calculate_avg_speed()
            genomes[x][1].fitness += car.calculate_reward(game_map)
            car.radar(game_map)
            car.Draw(game_map)

        if len(cars) == 0:
            break

        # Display generation information on the screen
        text = generation_font.render("Generation: " + str(generation), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (game_map.window_width / 2, 20)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(20)

if __name__ == "__main__":
    config_path = "config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run the car simulation using NEAT algorithm
    p.run(run_car, 40000000000000000)

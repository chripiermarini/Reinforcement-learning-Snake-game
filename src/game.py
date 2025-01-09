import pygame, sys, time, random
from pygame.surfarray import array3d

# setting colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


# setting game class
class SnakeEnv:

    def __init__(self, frame_size_x, frame_size_y):

        # setting the window sizes
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.game_window = pygame.display.set_mode(
            (self.frame_size_x, self.frame_size_y)
        )

        self.reset()
        pass

    def reset(self):
        """
        Reset execution.
        """

        # re-initiate the game, generating the snake in the beginning position and the food spawn
        self.game_window.fill(BLACK)
        self.snake_position = [100, 50]
        self.snake_body = [
            [100, 50],
            [100 - 10, 50],
            [100 - 20, 50],
        ]  # sequence of consecutive pixels
        self.food_position = self.spawn_food()
        self.food_spawn = True

        # the snake starts again at the beginning phase
        self.direction = "RIGHT"
        self.action = self.direction

        self.score = 0
        self.steps = 0
        print("Game reset!")

        pass

    def spawn_food(self):
        pass

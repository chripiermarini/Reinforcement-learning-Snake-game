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

    def change_direction(self, action, direction):
        """
        Method to avoid impossible action (repeated action or opposite direction)
        We first check that, given a specific requested action, the snake is not already going
        to the opposite direction, because the snake cannot perform 180° degrees direction changes.

        """

        if action == "UP" and direction != "DOWN":
            direction = "UP"
        if action == "DOWN" and direction != "UP":
            direction = "DOWN"
        if action == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        if action == "LEFT" and direction != "RIGHT":
            direction = "LEFT"

        return direction

    def move(self, direction, snake_pos):
        """
        The position of the snake can be defined through a list of two elements [x-axis, y-axis].
        If we wanted to change direction, given that the playable space is defined through numerical values
        multiple of 10, we just impose 'pos[0] + 10' to tell the snake to go right,
        'pos[0] - 10' to tell the snake to go left, etc.
        Bear in mind that the zero is in the angle to the top left corner!
        Hence, to go down, you increase the pos[1].
        """

        if direction == "UP":
            snake_pos[1] -= 10
        if direction == "DOWN":
            snake_pos[1] += 10
        if direction == "LEFT":
            snake_pos[0] -= 10
        if direction == "RIGHT":
            snake_pos[0] += 10

        return snake_pos

    def spawn_food(self):
        """
        Spawn the food pixel into a random position in the playable field.
        Each piece of food is ten pixel long, hence the " *10"
        """
        return [
            random.randrange(1, (self.frame_size_x // 10)) * 10,
            random.randrange(1, (self.frame_size_y // 10)) * 10,
        ]

    def eat(self):
        """
        The snake eats the food if the position of the head opf the snake is equal to the position of the food.
        We check that and if True."""
        return (self.snake_position[0] == self.food_position[0]) and (
            self.snake_position[1] == self.food_position[1]
        )

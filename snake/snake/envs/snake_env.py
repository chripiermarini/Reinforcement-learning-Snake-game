import pygame, sys, time, random
from colors import *
from pygame import display
from pygame.surfarray import array3d

import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding


# setting game class
class SnakeEnv(gym.Env):
    """
    Game environment that implements all the functions that are required to play
    the game.
    """

    metadata = {"render.modes": ["human"]}

    def __init__(self):

        # number of possible actions
        self.action_space = spaces.Discrete(4)

        # setting the window sizes
        self.frame_size_x = 200
        self.frame_size_y = 200
        self.game_window = pygame.display.set_mode(
            (self.frame_size_x, self.frame_size_y)
        )

        self.reset()

        # the game is going to be over if the agent performs 1000 steps
        self.STEP_LIMIT = 1000
        self.sleep = 0
        pass

    def reset(self):
        """
        Reset execution.
        It needs to return ONLY the observation image.
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

        self.direction = "RIGHT"
        self.action = self.direction

        self.score = 0
        self.steps = 0
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)

        return img

    @staticmethod
    def change_direction(action, direction):
        """
        Method to avoid impossible action (repeated action or opposite direction)
        We first check that, given a specific requested action, the snake is not already going
        to the opposite direction, because the snake cannot perform 180° degrees direction changes.
        """

        if action == 0 and direction != "DOWN":
            direction = "UP"
        if action == 1 and direction != "UP":
            direction = "DOWN"
        if action == 2 and direction != "LEFT":
            direction = "RIGHT"
        if action == 3 and direction != "RIGHT":
            direction = "LEFT"

        return direction

    @staticmethod
    def move(direction, snake_pos):
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

    def step(self, event):
        """
        Function that allows the agent to input an action to tell on the environment.
        """

        scoreholder = self.score
        reward = 0
        self.direction = SnakeEnv.change_direction(self.action, self.direction)

        self.snake_position = SnakeEnv.move(self.direction, self.snake_position)
        self.snake_body.insert(0, list(self.snake_position))

        reward = self.food_handler()

        self.update_game_state()

        reward, done = self.game_over(reward)

        img = self.get_image_array_from_game()

        info = {"score": self.score}
        self.steps += 1
        time.sleep(self.sleep)

        return img, reward, done, info

    def display_score(self, color, font, size):
        """
        Method that allow to print and see the score of the game.
        """

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render("Score: " + str(self.score), True, color)

        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 10, 15)  # top left corner
        self.game_window.blit(score_surface, score_rect)

        pass

    def food_handler(self):
        if self.eat():
            self.score += 1
            reward = 1
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward = 0

        if not self.food_spawn:
            self.food_position = self.spawn_food()
        self.food_spawn = True

        return reward

    def get_image_array_from_game(self):
        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0, 1)
        return img

    def update_game_state(self):
        """
        Update snake state.
        """
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(
                self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10)
            )

        pygame.draw.rect(
            self.game_window,
            WHITE,
            pygame.Rect(self.food_position[0], self.food_position[1], 10, 10),
        )
        pass

    def game_over(self, reward):
        """
        Method that performs the game over, which can happen either if the snake touches the box of the window
        or if the snake touches its own body.
        The first condition arises if the head of the snake is in the same position of the window edges
        The second condition happens if the snake head comes into contact
        with any possible part of the snake (that is not the head, that is).
        """

        if (
            self.snake_position[0] < 0
            or self.snake_position[0] > self.frame_size_x - 10
        ):
            return -1, True  # punish the agent, and ends the game
        if (
            self.snake_position[1] < 0
            or self.snake_position[1] > self.frame_size_y - 10
        ):
            return -1, True

        for block in self.snake_body[1:]:
            if (
                self.snake_position[0] == block[0]
                and self.snake_position[1] == block[1]
            ):
                return -1, True

        if self.steps >= self.STEP_LIMIT:
            return 0, True  # do not punish the agent, and ends the game

        return reward, False

    def end_game(self):
        """
        Prints the message that the game has ended, it comes up for four seconds, and then it ends the game.
        """

        # Prints the message
        message = pygame.font.SysFont("arial", 45)
        message_surface = message.render("Game over!", True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)

        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        self.display_score(RED, "times", 20)
        pygame.display.flip()
        time.sleep(4)
        pygame.quit()
        sys.exit()

        pass

    def render(self, mode="human"):
        if mode == "human":
            display.update()

    def close(self):
        pass

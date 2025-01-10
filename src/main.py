# first main file.
from game import SnakeEnv
import pygame
from colors import *
from pygame.surfarray import array3d


def main():

    # create the game
    snake_env = SnakeEnv(600, 600)

    # refresh rate
    difficulty = 10

    fps_controller = pygame.time.Clock()
    check_errors = pygame.init()

    pygame.display.set_caption("Snake Game")

    # set the logic
    while True:

        for event in pygame.event.get():
            snake_env.action = snake_env.human_action(event)

        # check human input
        snake_env.direction = snake_env.change_direction(
            snake_env.action, snake_env.direction
        )
        snake_env.snake_position = snake_env.move(
            snake_env.direction, snake_env.snake_position
        )

        # check if we ate food
        snake_env.snake_body.insert(0, list(snake_env.snake_position))
        if snake_env.eat():
            snake_env.score += 1
            snake_env.food_spawn = False
        else:
            snake_env.snake_body.pop()

        # check if spawn new food
        if not snake_env.food_spawn:
            snake_env.food_position = snake_env.spawn_food()
        snake_env.food_spawn = True

        # drawing the snake
        snake_env.game_window.fill(BLACK)
        for pos in snake_env.snake_body:
            pygame.draw.rect(
                snake_env.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10)
            )

        pygame.draw.rect(
            snake_env.game_window,
            WHITE,
            pygame.Rect(snake_env.food_position[0], snake_env.food_position[1], 10, 10),
        )
        
        # check if the game is over
        snake_env.game_over()
        
        # refresh game screen
        snake_env.display_score(WHITE, 'consolas', 20)
        
        pygame.display.update()
        fps_controller.tick(difficulty)
        img = array3d(snake_env.game_window)

    pass


if __name__ == "__main__":
    main()

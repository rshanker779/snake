import numpy as np
import pygame
from src.game.snake import GameState, run_game


class BotSnake(GameState):

    def __init__(self):
        super().__init__()
        self.choices = []

    def get_keys_pressed(self):
        keys = {}
        self.initialise_keys(keys)
        movement = self.get_best_movement()
        if movement == (1, 0):
            keys[pygame.K_RIGHT] = 1
        elif movement == (-1, 0):
            keys[pygame.K_LEFT] = 1
        elif movement == (0, 1):
            keys[pygame.K_UP] = 1
        elif movement == (0, -1):
            keys[pygame.K_DOWN] = 1
        return keys

    def get_best_movement(self):
        snake_location = (self.snake.head.rect.x, self.snake.head.rect.y)
        block_location = (self.block.rect.x, self.block.rect.y)
        best_dist = None
        best_movement = None
        for movement in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_dist = BotSnake.euclidean_method(np.add(movement, snake_location), block_location)
            if best_dist is None or next_dist < best_dist:
                best_movement = movement
                best_dist = next_dist
        return best_movement

    @staticmethod
    def euclidean_method(co_ord_1, co_ord_2):
        return np.sqrt(np.square(np.subtract(co_ord_1, co_ord_2)).sum())


def main():
    pygame.init()
    run_game(BotSnake())


if __name__ == '__main__':
    main()

from typing import Tuple
import numpy as np
import pygame
from src.game.snake import GameState


class GenericSnakeBot(GameState):
    """
    Class for a generic snake bot
    """

    def __init__(self):
        super().__init__()
        self.all_directions =  ((1, 0), (-1, 0), (0, 1), (0, -1))

    def get_keys_pressed(self):
        keys = {}
        self.initialise_keys(keys)
        movement = self.get_next_movement()
        if movement == (1, 0):
            keys[pygame.K_RIGHT] = 1
        elif movement == (-1, 0):
            keys[pygame.K_LEFT] = 1
        elif movement == (0, 1):
            keys[pygame.K_DOWN] = 1
        elif movement == (0, -1):
            keys[pygame.K_UP] = 1
        return keys

    def get_next_movement(self) -> Tuple[int]:
        raise NotImplementedError("Must implement a next movement function")


def euclidean_distance(co_ord_1, co_ord_2):
    return np.sqrt(np.square(np.subtract(co_ord_1, co_ord_2)).sum())



if __name__ == '__main__':
    pass

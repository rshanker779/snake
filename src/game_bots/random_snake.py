import random
import pygame
from src.game.snake import GameState, run_game


class RandomMovementState(GameState):
    def get_keys_pressed(self):
        keys = {}
        self.initialise_keys(keys)
        ran_choice = random.randint(0, 3)
        if ran_choice == 0:
            keys[pygame.K_LEFT] = 1
        elif ran_choice == 1:
            keys[pygame.K_RIGHT] = 1
        elif ran_choice == 2:
            keys[pygame.K_UP] = 1
        elif ran_choice == 3:
            keys[pygame.K_DOWN] = 1
        return keys




def main():
    pygame.init()
    run_game(RandomMovementState())
if __name__ == '__main__':
    main()
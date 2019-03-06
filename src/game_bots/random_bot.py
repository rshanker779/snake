import random
from src.game.snake import run_game
from src.game_bots.generic_snake_bot import GenericSnakeBot


class RandomMovementBot(GenericSnakeBot):

    def get_next_movement(self):
        return random.choice(self.all_directions)


def main():
    run_game(RandomMovementBot())

if __name__ == '__main__':
    main()
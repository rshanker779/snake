import numpy as np
from src.game.snake import run_game
from src.game_bots.generic_snake_bot import GenericSnakeBot, euclidean_distance


class EuclideanDistanceSnake(GenericSnakeBot):
    """
    Class for a snake bot that given a location, looks a possible moves and chooses closest one.
    """

    def get_next_movement(self):
        """Look through next possible locations and choose closest"""
        snake_location = (self.snake.head.rect.x, self.snake.head.rect.y)
        block_location = (self.block.rect.x, self.block.rect.y)
        best_dist = None
        best_movement = None
        for movement in self.all_directions:
            movement = tuple(movement)
            next_dist = euclidean_distance(np.add(movement, snake_location), block_location)
            if best_dist is None or next_dist < best_dist:
                best_movement = movement
                best_dist = next_dist
        return best_movement


def main():
    run_game(EuclideanDistanceSnake())


if __name__ == '__main__':
    main()

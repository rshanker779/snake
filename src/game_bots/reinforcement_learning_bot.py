from enum import Enum
import random
import numpy as np
from src.game.snake import run_game
from src.game_bots.generic_snake_bot import GenericSnakeBot, euclidean_distance


class Outcome(Enum):
    GOOD = 0
    BAD = 1


class BotParams:
    distance_threshold = 10


class ReinforcementSnake(GenericSnakeBot):

    def __init__(self):
        super().__init__()
        self.score_function = euclidean_distance
        self.memory_holder = set()

    def get_next_movement(self):
        memory = self.remember()
        if memory is None:
            next_direction = random.choice(self.all_directions)
        else:
            if memory.outcome == Outcome.GOOD:
                next_direction = memory.direction
            else:
                next_direction = random.choice([i for i in self.all_directions if i != memory.direction])
        current_score = self.score_function(self.snake_location, self.block_location)
        next_score = self.score_function(np.add(self.snake_location, next_direction), self.block_location)
        if current_score < next_score:
            outcome = Outcome.GOOD
        else:
            outcome = Outcome.BAD
        new_memory = Memory(self.snake_location, self.block_location, next_direction, outcome)
        self.memory_holder.add(new_memory)

    def remember(self):
        self.snake_location = (self.snake.head.rect.x, self.snake.head.rect.y)
        self.block_location = (self.block.rect.x, self.block.rect.y)
        best_memory = None
        best_distance = None
        for memory in self.memory_holder:
            head_distance = euclidean_distance(self.snake_location, memory.snake_location)
            block_distance = euclidean_distance(self.block_location, memory.block_location)
            if best_memory is None or head_distance * block_distance < best_distance:
                best_memory = memory
                best_distance = head_distance * block_distance
        if best_distance is not None and best_distance < 10:
            return best_memory
        return None


class Memory:
    def __init__(self, snake_location, block_location, direction, outcome):
        self.snake_location = snake_location
        self.block_location = block_location
        self.direction = direction
        self.outcome = outcome

    def __hash__(self):
        return hash((self.snake_location, self.block_location, self.direction, self.outcome))



def main():
    run_game(ReinforcementSnake())


if __name__ == '__main__':
    main()

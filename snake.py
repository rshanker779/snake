import pygame
from itertools import chain
from random import randrange


"""
TODO tidy up collision
Score on screen
Game over screen
"""
class Constants:
    SCREEN_X = 500
    SCREEN_Y = 500
    SCREEN_SIZE = (SCREEN_X, SCREEN_Y)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class SnakeParams:
    SNAKE_SQUARE_SIZE = 10
    SNAKE_SURFACE_SIZE = [SNAKE_SQUARE_SIZE] * 2
    SNAKE_STARTING_LOCATION = (250, 250)
    MOVEMENT_SPEED = 5
    MAX_SNAKE_LENGTH=10
    BLOCK_LAG = int(SNAKE_SQUARE_SIZE / MOVEMENT_SPEED)


class FoodParams:
    FOOD_SQUARE_SIZE = 5
    FOOD_CIRC_SIZE = [FOOD_SQUARE_SIZE, FOOD_SQUARE_SIZE]
    FOOD_SURFACE_SIZE = [10, 10]


class Scorer:
    def __init__(self, jump=10):
        self.score = 0
        self.jump = 10

    def jump_score(self):
        self.score += self.jump


class GenericBlock(pygame.sprite.Sprite):
    def __init__(self, block_size):
        super().__init__()
        self.image = pygame.Surface(block_size)
        self.image.fill(Constants.WHITE)
        self.image.set_colorkey(Constants.WHITE)
        self.rect = self.image.get_rect()


class GenericFoodBlock(GenericBlock):
    def __init__(self):
        super().__init__(FoodParams.FOOD_SURFACE_SIZE)
        pygame.draw.circle(self.image, Constants.BLACK, FoodParams.FOOD_CIRC_SIZE, FoodParams.FOOD_SQUARE_SIZE)


class GenericSnakeBlock(GenericBlock):
    def __init__(self):
        super().__init__(SnakeParams.SNAKE_SURFACE_SIZE)
        pygame.draw.rect(self.image, Constants.BLACK, [0, 0] + SnakeParams.SNAKE_SURFACE_SIZE, 0)
        self.snake_length = 0

class SnakeHead(GenericSnakeBlock):
    def __init__(self):
        super().__init__()
        self.rect.x, self.rect.y = SnakeParams.SNAKE_STARTING_LOCATION
        self.history_index = 0


class SnakeBlock(GenericSnakeBlock):
    def __init__(self):
        super().__init__()



class Snake:
    def __init__(self, snake_head):
        self.head = snake_head
        self.body = []
        self.new_segments = []
        self.head_history = []
        self.snake_length = 0

    def grow(self):
        if self.body:
            prev_segment = self.body[-1]
        else:
            prev_segment = self.head
        if prev_segment.history_index+SnakeParams.BLOCK_LAG<SnakeParams.BLOCK_LAG*SnakeParams.MAX_SNAKE_LENGTH:
            new_segment = SnakeBlock()
            prev_velocity = prev_segment.velocity
            prev_x = prev_segment.rect.x
            prev_y = prev_segment.rect.y
            new_segment.velocity = prev_segment.velocity
            new_segment.rect.x, new_segment.rect.y = get_added_direction(prev_velocity, prev_x, prev_y)
            new_segment.history_index = prev_segment.history_index + SnakeParams.BLOCK_LAG
            self.body.append(new_segment)
            self.new_segments.append(new_segment)
            self.snake_length+=1


    def set_velocity(self, new_velocity):
        self.head.velocity = new_velocity

    def move_snake(self):

        self.head.rect.x += SnakeParams.MOVEMENT_SPEED * self.head.velocity[0]
        self.head.rect.y += SnakeParams.MOVEMENT_SPEED * self.head.velocity[1]
        self.head.rect.x = compute_out_of_bound(self.head.rect.x, Constants.SCREEN_X)
        self.head.rect.y = compute_out_of_bound(self.head.rect.y, Constants.SCREEN_Y)
        if len(self.head_history)<SnakeParams.MAX_SNAKE_LENGTH * SnakeParams.BLOCK_LAG:
            self.head_history = [(self.head.rect.x, self.head.rect.y)] + self.head_history
        else:
            self.head_history = [(self.head.rect.x, self.head.rect.y)] + self.head_history[:-1]
        for segment in self.body:
            segment.rect.x, segment.rect.y = self.head_history[segment.history_index]

    def reset_new_segments(self):
        self.new_segments = []

    def __iter__(self):
        return chain([self.head], self.body)


def get_added_direction(velocity, x, y):
    if velocity == (1, 0):
        return x - SnakeParams.SNAKE_SQUARE_SIZE, y
    elif velocity == (-1, 0):
        return x + SnakeParams.SNAKE_SQUARE_SIZE, y
    elif velocity == (0, 1):
        return x, y - SnakeParams.SNAKE_SQUARE_SIZE
    elif velocity == (0, -1):
        return x, y + SnakeParams.SNAKE_SQUARE_SIZE


def compute_out_of_bound(co_ordinate, screen_limit):
    if co_ordinate < 0:
        co_ordinate += screen_limit
    if co_ordinate > screen_limit:
        co_ordinate -= screen_limit
    return co_ordinate


def main():
    pygame.init()
    snake = get_initial_snake()
    block = get_new_block()
    scorer = Scorer()
    sprite_list = pygame.sprite.Group()
    # Annoying having these seperate groups- for collisions
    snake_body_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    sprite_list.add(snake.head)
    for sprite in snake.body:
        sprite_list.add(sprite)
        snake_body_group.add(sprite)
        if snake.body:
            snake_body_group.remove(snake.body[0])
    sprite_list.add(block)
    # snake_head_group.add(snake.head)
    block_group.add(block)
    screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        food_collision_list = pygame.sprite.spritecollide(snake.head, block_group, True)
        if food_collision_list:
            block = act_on_food_collision(snake)
            scorer.jump_score()
            block_group.add(block)
            sprite_list.add(block)
        death_collision_list = pygame.sprite.spritecollide(snake.head, snake_body_group, True)
        if death_collision_list:
            print(death_collision_list)
        do_repeated_snake_action(snake)
        refresh_snake_sprites(sprite_list,snake_body_group, snake)
        screen.fill(Constants.WHITE)
        sprite_list.draw(screen)
        pygame.display.flip()
        # print(scorer.score)
        clock.tick(30)
    pygame.quit()


def get_initial_snake():
    snake = Snake(SnakeHead())
    snake.set_velocity((1, 0))
    return snake


def get_new_block():
    block = GenericFoodBlock()
    size = SnakeParams.SNAKE_SQUARE_SIZE
    block.rect.x = randrange(size, Constants.SCREEN_X - size, size)
    block.rect.y = randrange(size, Constants.SCREEN_Y - size, size)
    return block


def act_on_food_collision(snake):
    snake.grow()
    block = get_new_block()
    return block


def do_repeated_snake_action(snake):
    direction = snake.head.velocity

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if direction != (1, 0):
            direction = (-1, 0)
    if keys[pygame.K_RIGHT]:
        if direction != (-1, 0):
            direction = (1, 0)
    if keys[pygame.K_DOWN]:
        if direction != (0, -1):
            direction = (0, 1)
    if keys[pygame.K_UP]:
        if direction != (0, 1):
            direction = (0, -1)
    snake.set_velocity(direction)
    snake.move_snake()


def refresh_snake_sprites(sprite_list, body_list, snake):
    for segment in snake.new_segments:
        sprite_list.add(segment)
        body_list.add(segment)
    if snake.body:
        body_list.remove(snake.body[0])
    snake.reset_new_segments()


if __name__ == '__main__':
    main()

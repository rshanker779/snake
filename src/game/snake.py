from random import randrange
import pygame


class Constants:
    """
    Class of fixed constants with some names to avoid magic numbering
    """
    SCREEN_X = 400
    SCREEN_Y = 400
    SCREEN_SIZE = (SCREEN_X, SCREEN_Y)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    CLOCK_TICK = 25
    DIE_ON_WALL = False


class SnakeParams:
    """
    Class for snake parameters
    """
    SNAKE_SQUARE_SIZE = 8
    SNAKE_SURFACE_SIZE = [SNAKE_SQUARE_SIZE] * 2
    SNAKE_STARTING_LOCATION = (250, 250)
    MOVEMENT_SPEED = SNAKE_SQUARE_SIZE
    MAX_SNAKE_LENGTH = 100
    BLOCK_LAG = int(SNAKE_SQUARE_SIZE / MOVEMENT_SPEED)
    COLOUR = Constants.BLACK


class FoodParams:
    """
    Class for food parameters
    """
    FOOD_RADIUS = int(SnakeParams.SNAKE_SQUARE_SIZE / 2)
    FOOD_CIRC_SIZE = [FOOD_RADIUS, FOOD_RADIUS]
    FOOD_SURFACE_SIZE = [2 * FOOD_RADIUS, 2 * FOOD_RADIUS]
    COLOUR = Constants.RED


class FontParams:
    """
    Default font settings any text based class should inherit
    """
    FONT = 'Arial'
    FONT_SIZE = 20
    FONT_COLOUR = Constants.BLACK


class ScoreParams(FontParams):
    """Class for score box parameters"""
    SCORE_SURFACE_SIZE = [10, 10]
    LOCATION = (Constants.SCREEN_X - 50, Constants.SCREEN_Y - 50)


class GameOverParams(FontParams):
    """Class for Game over display parameters"""
    SURFACE_SIZE = Constants.SCREEN_SIZE


class StartGameParams(FontParams):
    """ Class for start screen params"""
    SURFACE_SIZE = Constants.SCREEN_SIZE
    LOCATION = (0, 0)


class Scorer:
    """Class to keep hold of game score"""

    def __init__(self, jump=10):
        self.score = 0
        self.jump = jump

    def jump_score(self):
        self.score += self.jump


class GenericBlock(pygame.sprite.Sprite):
    """Block with some shared code we want across all blocks"""

    def __init__(self, block_size):
        super().__init__()
        self.image = pygame.Surface(block_size)
        self.image.fill(Constants.WHITE)
        self.image.set_colorkey(Constants.WHITE)
        self.get_rect()

    def get_rect(self, *args, **kwargs):
        self.rect = self.image.get_rect(*args, **kwargs)


class TextBox(GenericBlock):
    """Generic holder for text elements"""

    def __init__(self, surface_size, font, font_size, text):
        super().__init__(surface_size)
        self.font = pygame.font.SysFont(font, font_size)
        self.text = text

    def set_text(self, text):
        self.text = text


class ScoreBox(TextBox):
    def __init__(self, text=''):
        super().__init__(ScoreParams.SCORE_SURFACE_SIZE, ScoreParams.FONT, ScoreParams.FONT_SIZE, text)


class GameOverBox(TextBox):
    def __init__(self, text=''):
        super().__init__(GameOverParams.SURFACE_SIZE, GameOverParams.FONT,
                         GameOverParams.FONT_SIZE, text)


class StartGameBox(TextBox):
    def __init__(self, text=''):
        super().__init__(StartGameParams.SURFACE_SIZE, StartGameParams.FONT,
                         StartGameParams.FONT_SIZE, text)


class FoodBlock(GenericBlock):
    """Ciruclar food block snake will eat"""

    def __init__(self):
        super().__init__(FoodParams.FOOD_SURFACE_SIZE)
        pygame.draw.circle(self.image, FoodParams.COLOUR, FoodParams.FOOD_CIRC_SIZE, FoodParams.FOOD_RADIUS)


class GenericSnakeBlock(GenericBlock):
    def __init__(self):
        super().__init__(SnakeParams.SNAKE_SURFACE_SIZE)
        pygame.draw.rect(self.image, SnakeParams.COLOUR, [0, 0] + SnakeParams.SNAKE_SURFACE_SIZE, 0)
        self.snake_length = 0


class SnakeHead(GenericSnakeBlock):
    """Snake head we will move """

    def __init__(self):
        super().__init__()
        self.rect.x, self.rect.y = SnakeParams.SNAKE_STARTING_LOCATION
        self.history_index = 0


class SnakeBodyBlock(GenericSnakeBlock):
    """Snake body we will grow"""

    def __init__(self):
        super().__init__()


class Snake:
    """
    A snake is a head, and a series of segments, the body, and some methods that dictate
    how the snake moves
    """

    def __init__(self, snake_head):
        """Initially a snake is just a head"""
        self.head = snake_head
        self.body = []
        self.new_segments = []
        self.head_history = []
        self.snake_length = 0
        self.stop = False
        self.hit_wall = False

    def grow(self):
        """Method that adds a segment to the body. Decides where the body needs to be located, and what index
        of the head_history list we refer to
        """
        if self.body:
            prev_segment = self.body[-1]
        else:
            prev_segment = self.head
        if prev_segment.history_index + SnakeParams.BLOCK_LAG < SnakeParams.BLOCK_LAG * SnakeParams.MAX_SNAKE_LENGTH:
            new_segment = SnakeBodyBlock()
            new_segment.history_index = prev_segment.history_index + SnakeParams.BLOCK_LAG
            new_segment.rect.x, new_segment.rect.y = self.head_history[new_segment.history_index]
            self.body.append(new_segment)
            # This line makes sure the first body segment is not considered new- this is for convenience, as otherwise
            # snake instantly dies as head and first block touch
            if self.body:
                self.new_segments.append(new_segment)
            self.snake_length += 1

    def set_direction(self, new_direction):
        self.head.direction = new_direction

    def move_snake(self):
        """
        Moving a snake- Basic idea is we only explicity move the head- the head has a direction, and each frame
        we make a step in that direction. We hold a lost of the historic positions of the head, and use this to decide
        where the body should go
        """
        if not self.stop:
            self.head.rect.x += SnakeParams.MOVEMENT_SPEED * self.head.direction[0]
            self.head.rect.y += SnakeParams.MOVEMENT_SPEED * self.head.direction[1]
            if not Constants.DIE_ON_WALL:
                self.head.rect.x = self.compute_out_of_bound(self.head.rect.x, Constants.SCREEN_X)
                self.head.rect.y = self.compute_out_of_bound(self.head.rect.y, Constants.SCREEN_Y)
            else:
                if self.is_out_of_bounds(self.head.rect.x, Constants.SCREEN_X) or self.is_out_of_bounds(
                        self.head.rect.y, Constants.SCREEN_Y):
                    self.hit_wall = True
            if len(self.head_history) < SnakeParams.MAX_SNAKE_LENGTH * SnakeParams.BLOCK_LAG:
                self.head_history = [(self.head.rect.x, self.head.rect.y)] + self.head_history
            else:
                self.head_history = [(self.head.rect.x, self.head.rect.y)] + self.head_history[:-1]
            for segment in self.body:
                segment.rect.x, segment.rect.y = self.head_history[segment.history_index]

    def reset_new_segments(self):
        self.new_segments = []

    def stop_snake(self):
        self.stop = True

    @staticmethod
    def compute_out_of_bound(co_ordinate, screen_limit):
        """Loop screen when we go out of bounds"""
        if co_ordinate < 0:
            co_ordinate += screen_limit
        if co_ordinate > screen_limit:
            co_ordinate -= screen_limit
        return co_ordinate

    @staticmethod
    def is_out_of_bounds(co_ordinate, screen_limit):
        return co_ordinate < 0 or co_ordinate > screen_limit


class GameState:
    """Class to hold snake and food objects we need in our game state"""

    def __init__(self):
        pygame.init()
        self.game_start = False
        self.start_screen = StartGameBox("Press p to play")
        self.game_over = False
        self.get_initial_snake()
        self.score_box = ScoreBox('0')
        self.get_new_block()
        self.scorer = Scorer()
        self.initialise_sprite_groups()
        self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def initialise_sprite_groups(self):
        """Set up sprite groups to track different game elements"""
        self.sprite_group = pygame.sprite.Group()
        self.snake_body_group = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.sprite_group.add(self.snake.head)
        self.sprite_group.add(self.score_box)
        if self.snake.body:
            for sprite in self.snake.body[1:]:
                self.sprite_group.add(sprite)
                self.snake_body_group.add(sprite)
        self.sprite_group.add(self.block)
        self.block_group.add(self.block)

    def get_initial_snake(self):
        """Initiates a basic snake"""
        snake = Snake(SnakeHead())
        snake.set_direction((1, 0))
        self.snake = snake

    def get_new_block(self):
        """Method to get a new food block in random location"""
        block = FoodBlock()
        size = SnakeParams.SNAKE_SQUARE_SIZE
        block.rect.left = randrange(size, Constants.SCREEN_X - size, size)
        block.rect.top = randrange(size, Constants.SCREEN_Y - size, size)
        self.block = block

    def do_repeated_action(self):
        """Main logic executed each frame"""
        if self.game_start:
            self.act_on_death_collision()
            self.act_on_wall_collision()
            self.act_on_food_collision()
            self.do_repeated_snake_action()
            self.refresh_snake_sprites()
            self.screen.blit(self.score_box.font.render(self.score_box.text, True, ScoreParams.FONT_COLOUR),
                             ScoreParams.LOCATION)

        else:
            # If not started, wait for input key and then start
            self.screen.blit(self.start_screen.font.render(self.start_screen.text, True, StartGameParams.FONT_COLOUR),
                             StartGameParams.LOCATION)
            keys = self.get_keys_pressed()
            if keys[pygame.K_p]:
                self.game_start = True
        self.update_display()

    def act_on_food_collision(self):
        """When we hit some food we grow, get more food, and adjust score """
        food_collision_list = pygame.sprite.spritecollide(self.snake.head, self.block_group, True)
        if food_collision_list:
            self.snake.grow()
            self.get_new_block()
            self.scorer.jump_score()
            self.score_box.set_text(str(self.scorer.score))
            self.block_group.add(self.block)
            self.sprite_group.add(self.block)

    def act_on_death_collision(self):
        """On death we stop snake and end game"""
        death_collision_list = pygame.sprite.spritecollide(self.snake.head, self.snake_body_group, True)
        if death_collision_list:
            self.snake.stop_snake()
            self.game_over_death()

    def act_on_wall_collision(self):
        """Check if wall is hit then stop snake and end game"""
        if self.snake.hit_wall:
            self.snake.stop_snake()
            self.game_over_death()

    def do_repeated_snake_action(self):
        """Update the direction of the head based on key press"""
        direction = self.snake.head.direction
        keys = self.get_keys_pressed()
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
        if keys[pygame.K_x]:
            self.game_over_death()
        self.snake.set_direction(direction)
        self.snake.move_snake()

    def get_keys_pressed(self):
        keys = pygame.key.get_pressed()
        return keys

    def initialise_keys(self, keys):
        """Method for bots to initialise keys used in games"""
        keys[pygame.K_p] = 1  # To start game if not already started
        keys[pygame.K_LEFT] = 0
        keys[pygame.K_RIGHT] = 0
        keys[pygame.K_UP] = 0
        keys[pygame.K_DOWN] = 0
        keys[pygame.K_x] = 0

    def refresh_snake_sprites(self):
        """Add any new segments to sprite groups, and clear new segments"""
        for segment in self.snake.new_segments:
            self.sprite_group.add(segment)
            self.snake_body_group.add(segment)
        self.snake.reset_new_segments()

    def update_display(self):
        """Redraw sprites and refresh display"""
        pygame.display.flip()
        self.screen.fill(Constants.WHITE)
        self.sprite_group.draw(self.screen)
        self.clock.tick(Constants.CLOCK_TICK)

    def game_over_death(self):
        """On game over, we show game over screen, then pause for 5s, then end game"""
        game_over_box = GameOverBox('Game over, score {} '.format(self.scorer.score))
        game_over_box.get_rect(center=(Constants.SCREEN_X / 2, Constants.SCREEN_Y / 2))
        self.screen.blit(game_over_box.font.render(game_over_box.text, True, GameOverParams.FONT_COLOUR),
                         [(Constants.SCREEN_X - game_over_box.rect.width) / 2,
                          (Constants.SCREEN_Y - game_over_box.rect.height) / 2])
        self.update_display()
        pygame.time.delay(5000)
        self.game_over = True


def run_game(game_state):
    while not game_state.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.game_over = True
        game_state.do_repeated_action()
    pygame.quit()

def main():
    """Main event loop function"""
    game_state = GameState()
    run_game(game_state)


if __name__ == '__main__':
    main()

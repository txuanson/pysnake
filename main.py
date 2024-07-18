"""
PySnake
Author: sxntrxn (tranxuanson2013@gmail.com)
"""

import pygame as pg
from pygame.math import Vector2

from abc import ABC, abstractmethod
from random import randint
from typing import Tuple

# Configuration screen
CELL_SIZE = 32
TOP_OFFSET = CELL_SIZE * 5
HORIZONTAL_OFFSET = CELL_SIZE
BOT_OFFSET = CELL_SIZE * 2

# Text shadow offset
TEXT_SHADOW_OFFSET = 4

# User's Input
CELL_HORIZONTAL_COUNTONTAL_COUNT = 0
CELL_VERTICAL_COUNT = 0

while CELL_HORIZONTAL_COUNTONTAL_COUNT <= 3:
    CELL_HORIZONTAL_COUNTONTAL_COUNT = int(
        input("Enter the horizontal count of cells: ")
    )
    if CELL_HORIZONTAL_COUNTONTAL_COUNT <= 3:
        print("Invalid input. Please enter a number greater than 3.")

while CELL_VERTICAL_COUNT <= 3:
    CELL_VERTICAL_COUNT = int(input("Enter the vertical count of cells: "))
    if CELL_VERTICAL_COUNT <= 3:
        print("Invalid input. Please enter a number greater than 3.")

# Calculate the width and height of the screen
PLAY_AREA_WIDTH = CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_SIZE
PLAY_AREA_HEIGHT = CELL_VERTICAL_COUNT * CELL_SIZE
WIDTH = PLAY_AREA_WIDTH + 2 * HORIZONTAL_OFFSET
HEIGHT = PLAY_AREA_HEIGHT + TOP_OFFSET + BOT_OFFSET

# Direction constants
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

# Initialize the pg engine
pg.init()


# Loading resources
def load_resources(path: str) -> pg.Surface:
    return pg.transform.scale(pg.image.load(path), (CELL_SIZE, CELL_SIZE))


# Load sprites
ICON = load_resources("resources/icon.png")
SNAKE = {
    # Head
    "HEAD_UP": load_resources("resources/sprites/snake/head_up.png"),
    "HEAD_DOWN": load_resources("resources/sprites/snake/head_down.png"),
    "HEAD_LEFT": load_resources("resources/sprites/snake/head_left.png"),
    "HEAD_RIGHT": load_resources("resources/sprites/snake/head_right.png"),
    # Body
    "BODY_HORIZONTAL": load_resources("resources/sprites/snake/body_horizontal.png"),
    "BODY_VERTICAL": load_resources("resources/sprites/snake/body_vertical.png"),
    "BODY_TOP_LEFT": load_resources("resources/sprites/snake/body_tl.png"),
    "BODY_TOP_RIGHT": load_resources("resources/sprites/snake/body_tr.png"),
    "BODY_BOTTOM_LEFT": load_resources("resources/sprites/snake/body_bl.png"),
    "BODY_BOTTOM_RIGHT": load_resources("resources/sprites/snake/body_br.png"),
    # Tail
    "TAIL_UP": load_resources("resources/sprites/snake/tail_up.png"),
    "TAIL_DOWN": load_resources("resources/sprites/snake/tail_down.png"),
    "TAIL_LEFT": load_resources("resources/sprites/snake/tail_left.png"),
    "TAIL_RIGHT": load_resources("resources/sprites/snake/tail_right.png"),
}
FOOD_SPRITE = load_resources("resources/sprites/food.png")
FENCE_SPRITE = {
    "VERTICAL_MID": load_resources("resources/sprites/fences/fence_vertical_mid.png"),
    "HORIZONTAL_MID": load_resources(
        "resources/sprites/fences/fence_horizontal_mid.png"
    ),
    "TOP_LEFT": load_resources("resources/sprites/fences/fence_top_left.png"),
    "TOP_RIGHT": load_resources("resources/sprites/fences/fence_top_right.png"),
    "BOT_LEFT": load_resources("resources/sprites/fences/fence_bot_left.png"),
    "BOT_RIGHT": load_resources("resources/sprites/fences/fence_bot_right.png"),
}

# Snake's direction mapping
SNAKE_HEAD = {
    tuple(UP): SNAKE["HEAD_UP"],
    tuple(DOWN): SNAKE["HEAD_DOWN"],
    tuple(LEFT): SNAKE["HEAD_LEFT"],
    tuple(RIGHT): SNAKE["HEAD_RIGHT"],
}

SNAKE_TAIL = {
    tuple(UP): SNAKE["TAIL_UP"],
    tuple(DOWN): SNAKE["TAIL_DOWN"],
    tuple(LEFT): SNAKE["TAIL_LEFT"],
    tuple(RIGHT): SNAKE["TAIL_RIGHT"],
}

SNAKE_BODY = {
    # Going in the straight line
    tuple((tuple(UP), tuple(UP))): SNAKE["BODY_VERTICAL"],
    tuple((tuple(DOWN), tuple(DOWN))): SNAKE["BODY_VERTICAL"],
    tuple((tuple(LEFT), tuple(LEFT))): SNAKE["BODY_HORIZONTAL"],
    tuple((tuple(RIGHT), tuple(RIGHT))): SNAKE["BODY_HORIZONTAL"],
    # Curve
    tuple((tuple(UP), tuple(LEFT))): SNAKE["BODY_TOP_RIGHT"],
    tuple((tuple(UP), tuple(RIGHT))): SNAKE["BODY_TOP_LEFT"],
    tuple((tuple(DOWN), tuple(LEFT))): SNAKE["BODY_BOTTOM_RIGHT"],
    tuple((tuple(DOWN), tuple(RIGHT))): SNAKE["BODY_BOTTOM_LEFT"],
    tuple((tuple(LEFT), tuple(UP))): SNAKE["BODY_BOTTOM_LEFT"],
    tuple((tuple(LEFT), tuple(DOWN))): SNAKE["BODY_TOP_LEFT"],
    tuple((tuple(RIGHT), tuple(UP))): SNAKE["BODY_BOTTOM_RIGHT"],
    tuple((tuple(RIGHT), tuple(DOWN))): SNAKE["BODY_TOP_RIGHT"],
}


# Search snake mapping
def search_snake_mapping(
    d: dict[tuple, pg.Surface], *directions: Vector2
) -> pg.Surface:
    if len(directions) == 1:
        direction = tuple(directions[0])
        if direction in d:
            return d[direction]
        raise Exception(f"Direction {direction} not found in the mapping")
    else:
        direction = tuple(list(tuple(_direction) for _direction in directions))
        if direction in d:
            return d[direction]
        raise Exception(f"Direction {direction} not found in the mapping")


# Set up the drawing window
screen = pg.display.set_mode(size=[WIDTH, HEIGHT])
pg.display.set_caption("PySnake")
pg.display.set_icon(ICON)

# Set up clock
clock = pg.time.Clock()


def calculate_position(x: int, y: int) -> Tuple[int, int]:
    return x * CELL_SIZE + HORIZONTAL_OFFSET, y * CELL_SIZE + TOP_OFFSET


# Check if the target is within the boundaries of the top_left and bottom_right
def check_collision(target: Vector2, top_left: Vector2, bottom_right: Vector2) -> bool:
    return (
        top_left.x <= target.x < bottom_right.x
        and top_left.y <= target.y < bottom_right.y
    )


# Generate a random position for the food that is not colliding with the snake
def generate_food_position(snake_body: list[Vector2], size: int) -> Vector2:
    failed_attempts = 0
    while True:
        pos_x = randint(0, CELL_HORIZONTAL_COUNTONTAL_COUNT - size)
        pos_y = randint(0, CELL_VERTICAL_COUNT - size)
        pos = Vector2(pos_x, pos_y)
        if all(
            not check_collision(body_part, pos, pos + Vector2(size, size))
            for body_part in snake_body
        ):
            return pos
        failed_attempts += 1
        if failed_attempts > 100:
            return None


class GameObject(ABC):
    @abstractmethod
    def draw(self):
        pass


class Snake(GameObject):
    body: list[Vector2] = [Vector2(0, 0), Vector2(1, 0), Vector2(2, 0)]
    # The intended direction of the snake, this will be updated to the current direction every tick
    direction = RIGHT
    # The current direction of the snake
    current_direction = RIGHT
    # Flag to increase the length of the snake
    increase_in_next_tick = False

    def __init__(self):
        super(Snake, self).__init__()

    def draw(self):
        # Draw the head
        head = search_snake_mapping(SNAKE_HEAD, self.current_direction)
        translated_pos = calculate_position(self.body[-1].x, self.body[-1].y)
        head_rect = pg.rect.Rect(
            translated_pos[0], translated_pos[1], CELL_SIZE, CELL_SIZE
        )
        screen.blit(head, head_rect)

        # Draw the body
        for body_index in range(1, len(self.body) - 1):
            # Get the direction of the body part
            first_body_part_direction = (
                self.body[body_index] - self.body[body_index - 1]
            )
            second_body_part_direction = (
                self.body[body_index + 1] - self.body[body_index]
            )
            # print(f"Body part direction: {body_part_direction}")
            body = search_snake_mapping(
                SNAKE_BODY, first_body_part_direction, second_body_part_direction
            )

            translated_pos = calculate_position(
                self.body[body_index].x, self.body[body_index].y
            )
            body_rect = pg.rect.Rect(
                translated_pos[0], translated_pos[1], CELL_SIZE, CELL_SIZE
            )
            screen.blit(body, body_rect)

        # Draw the tail
        tail_direction = self.body[1] - self.body[0]
        tail = search_snake_mapping(SNAKE_TAIL, tail_direction)
        translated_pos = calculate_position(self.body[0].x, self.body[0].y)
        tail_rect = pg.rect.Rect(
            translated_pos[0], translated_pos[1], CELL_SIZE, CELL_SIZE
        )
        screen.blit(tail, tail_rect)

    def move(self):
        # Update the current direction
        self.current_direction = self.direction

        # Increase the length of the snake if the flag is set and clear the flag
        # Also do a circuit break to prevent the snake from going forward
        if self.increase_in_next_tick:
            self.increase_in_next_tick = False
            new_head = self.body[-1] + self.current_direction
            body_copy = self.body[:]
            body_copy.append(new_head)
            self.body = body_copy[:]
            return

        # Copy the body parts of the snake except the tail
        body_copy = self.body[1:]
        # Calculate the new head based on the current direction
        new_head = self.body[-1] + self.current_direction
        # Insert the new head at the last position
        body_copy.append(new_head)
        # Update the body
        self.body = body_copy[:]


class Food(GameObject):
    # size of the food intended to make the food bigger (like the childhood Nokia snake game)
    def __init__(self, snake_body: list[Vector2], size: int = 1):
        super(Food, self).__init__()
        self.pos = generate_food_position(snake_body, size)
        self.size = size

    def draw(self):
        translated_pos = calculate_position(self.pos.x, self.pos.y)
        food_rect = pg.rect.Rect(
            translated_pos[0],
            translated_pos[1],
            CELL_SIZE * self.size,
            CELL_SIZE * self.size,
        )
        screen.blit(FOOD_SPRITE, food_rect)

    def update(self, pos: Vector2):
        self.pos = pos


class Game:
    # The current state of the game
    # NOT_YET_STARTED: The game has not started yet
    # RUNNING: The game is running
    # PAUSED: The game is paused
    # GAME_OVER: The game is over
    state = "NOT_YET_STARTED"

    def __init__(self):
        self.init()

    def init(self):
        self.snake = Snake()
        self.food = Food(self.snake.body, 1)

    def start(self):
        self.init()
        self.state = "RUNNING"

    def tick(self):
        if self.state != "RUNNING":
            return

        self.snake.move()

        # Check if the snake cover the whole board
        if (
            len(self.snake.body) - 3
            == CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_VERTICAL_COUNT
        ):
            self.state = "GAME_OVER"
            return

        # Check if the snake has collided with itself
        if any(
            check_collision(self.snake.body[-1], body_part, body_part + Vector2(1, 1))
            for body_part in self.snake.body[:-1]
        ):
            game.state = "GAME_OVER"
            return

        # Check if the snake has collided with the boundaries
        if not check_collision(
            self.snake.body[-1],
            Vector2(0, 0),
            Vector2(CELL_HORIZONTAL_COUNTONTAL_COUNT, CELL_VERTICAL_COUNT),
        ):
            game.state = "GAME_OVER"
            return

        if check_collision(
            self.snake.body[-1],
            self.food.pos,
            self.food.pos + Vector2(self.food.size, self.food.size),
        ):
            self.snake.increase_in_next_tick = True
            self.food.update(generate_food_position(self.snake.body, self.food.size))

    def change_snake_direction(self, direction: Vector2):
        self.snake.direction = direction

    def get_snake_direction(self) -> Vector2:
        return self.snake.current_direction

    def draw(self):
        screen.fill((65, 152, 10))

        if self.state == "NOT_YET_STARTED":
            self.draw_start_screen()
            return

        if self.state == "GAME_OVER":
            self.draw_game_over()
            return

        self.draw_board()
        self.draw_fence()
        self.draw_score()

        self.snake.draw()
        self.food.draw()

    def draw_start_screen(self):
        game_name_font = pg.font.Font(None, 48)
        # Draw the shadow of the text
        game_name_text = game_name_font.render("Press SPACE to start", True, (0, 0, 0))
        game_name_text_rect = game_name_text.get_rect(
            center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, HEIGHT // 2)
        )
        screen.blit(game_name_text, game_name_text_rect)
        # Draw the actual text
        game_name_text = game_name_font.render(
            "Press SPACE to start", True, (255, 255, 255)
        )
        game_name_text_rect = game_name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_name_text, game_name_text_rect)

    def draw_board(self):
        for x in range(CELL_HORIZONTAL_COUNTONTAL_COUNT):
            for y in range(x % 2, CELL_VERTICAL_COUNT, 2):
                cell_rect = pg.rect.Rect(
                    x * CELL_SIZE + HORIZONTAL_OFFSET,
                    y * CELL_SIZE + TOP_OFFSET,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pg.draw.rect(screen, (0, 100, 0), cell_rect)

    def draw_fence(self):
        # Draw the horizontal fence
        screen.blit(
            FENCE_SPRITE["TOP_LEFT"],
            (HORIZONTAL_OFFSET - CELL_SIZE, TOP_OFFSET - CELL_SIZE),
        )
        screen.blit(
            FENCE_SPRITE["BOT_LEFT"],
            (HORIZONTAL_OFFSET - CELL_SIZE, HEIGHT - BOT_OFFSET),
        )
        for x in range(CELL_HORIZONTAL_COUNTONTAL_COUNT):
            # Draw the top fence
            screen.blit(
                FENCE_SPRITE["HORIZONTAL_MID"],
                (x * CELL_SIZE + HORIZONTAL_OFFSET, TOP_OFFSET - CELL_SIZE),
            )
            # Draw the bottom fence
            screen.blit(
                FENCE_SPRITE["HORIZONTAL_MID"],
                (x * CELL_SIZE + HORIZONTAL_OFFSET, HEIGHT - BOT_OFFSET),
            )
        screen.blit(
            FENCE_SPRITE["TOP_RIGHT"],
            (
                CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_SIZE + HORIZONTAL_OFFSET,
                TOP_OFFSET - CELL_SIZE,
            ),
        )
        screen.blit(
            FENCE_SPRITE["BOT_RIGHT"],
            (
                CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_SIZE + HORIZONTAL_OFFSET,
                HEIGHT - BOT_OFFSET,
            ),
        )

        # Draw the vertical fences
        for y in range(CELL_VERTICAL_COUNT):
            screen.blit(
                FENCE_SPRITE["VERTICAL_MID"],
                (HORIZONTAL_OFFSET - CELL_SIZE, y * CELL_SIZE + TOP_OFFSET),
            )
            screen.blit(
                FENCE_SPRITE["VERTICAL_MID"],
                (
                    CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_SIZE + HORIZONTAL_OFFSET,
                    y * CELL_SIZE + TOP_OFFSET,
                ),
            )

    def draw_score(self):
        # Draw the score panel
        score_panel_rect = pg.rect.Rect(
            HORIZONTAL_OFFSET - (CELL_SIZE // 2),
            CELL_SIZE // 2,
            PLAY_AREA_WIDTH + CELL_SIZE,
            TOP_OFFSET - 2 * CELL_SIZE,
        )
        pg.draw.rect(screen, (255, 255, 255), score_panel_rect, 2)

        # Draw the game name and the author under
        game_name_font = pg.font.Font(None, 48)
        # Draw the shadow of the text
        game_name_text = game_name_font.render("PySnake", True, (0, 0, 0))
        game_name_text_rect = game_name_text.get_rect(
            center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(game_name_text, game_name_text_rect)
        # Draw the actual text
        game_name_text = game_name_font.render("PySnake", True, (255, 255, 255))
        game_name_text_rect = game_name_text.get_rect(
            center=(WIDTH // 2, CELL_SIZE + CELL_SIZE // 2)
        )
        screen.blit(game_name_text, game_name_text_rect)

        # Draw the score text
        score_font = pg.font.Font(None, 36)
        score_text = score_font.render(
            f"Score: {len(self.snake.body) - 3}", True, (255, 255, 255)
        )
        score_text_rect = score_text.get_rect(
            center=(WIDTH // 2, TOP_OFFSET // 2 + CELL_SIZE // 2)
        )
        screen.blit(score_text, score_text_rect)

        # Draw the instruction to pause the game
        pause_font = pg.font.Font(None, 24)
        pause_text = pause_font.render(
            (
                "Press SPACE to pause"
                if self.state == "RUNNING"
                else "Press SPACE to resume"
            ),
            True,
            (255, 255, 255),
        )
        pause_text_rect = pause_text.get_rect(
            center=(
                WIDTH // 2,
                TOP_OFFSET + PLAY_AREA_HEIGHT + CELL_SIZE + CELL_SIZE // 2,
            )
        )
        screen.blit(pause_text, pause_text_rect)

    def draw_game_over(self):
        game_over_font = pg.font.Font(None, 48)
        # Draw the shadow of the text
        game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect(
            center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, HEIGHT // 2 - 2 * CELL_SIZE)
        )
        screen.blit(game_over_text, game_over_text_rect)
        # Draw the actual text
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 2 * CELL_SIZE)
        )
        screen.blit(game_over_text, game_over_text_rect)

        # Draw the score text
        score_font = pg.font.Font(None, 36)
        score_text = score_font.render(
            f"Score: {len(self.snake.body) - 3}", True, (255, 255, 255)
        )
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_text, score_text_rect)

        # Draw the win or lose message
        if (
            len(self.snake.body) - 3
            == CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_VERTICAL_COUNT
        ):
            win_font = pg.font.Font(None, 36)
            # Draw the shadow of the text
            win_text = win_font.render("You Win!", True, (0, 0, 0))
            win_text_rect = win_text.get_rect(
                center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, HEIGHT // 2 + 4 * CELL_SIZE)
            )
            screen.blit(win_text, win_text_rect)
            # Draw the actual text
            win_text = win_font.render("You Win!", True, (255, 255, 255))
            win_text_rect = win_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 4 * CELL_SIZE)
            )
            screen.blit(win_text, win_text_rect)
        else:
            lose_font = pg.font.Font(None, 36)
            # Draw the shadow of the text
            lose_text = lose_font.render("You Lose!", True, (0, 0, 0))
            lose_text_rect = lose_text.get_rect(
                center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, HEIGHT // 2 + 4 * CELL_SIZE)
            )
            screen.blit(lose_text, lose_text_rect)
            # Draw the actual text
            lose_text = lose_font.render("You Lose!", True, (255, 255, 255))
            lose_text_rect = lose_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 4 * CELL_SIZE)
            )
            screen.blit(lose_text, lose_text_rect)

        # Draw the instruction to restart the game
        restart_font = pg.font.Font(None, 24)
        # Draw the shadow of the text
        restart_text = restart_font.render("Press SPACE to restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(
            center=(WIDTH // 2 + TEXT_SHADOW_OFFSET, HEIGHT // 2 + 6 * CELL_SIZE)
        )
        screen.blit(restart_text, restart_text_rect)

    def on_space_pressed(self):
        if self.state == "GAME_OVER" or self.state == "NOT_YET_STARTED":
            self.start()
        else:
            self.state = "PAUSED" if self.state == "RUNNING" else "RUNNING"


# User events
GAME_TICK = pg.USEREVENT
# Set the tickrate of the game
TICKRATE = 1
pg.time.set_timer(GAME_TICK, 1000 // TICKRATE)
game = Game()

# Run until the user asks to quit
running = True
while running:

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Move thticke everytick
        if event.type == GAME_TICK:
            game.tick()
        # Handle key press events
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game.get_snake_direction().y == 0:
                game.change_snake_direction(UP)
            if event.key == pg.K_DOWN and game.get_snake_direction().y == 0:
                game.change_snake_direction(DOWN)
            if event.key == pg.K_LEFT and game.get_snake_direction().x == 0:
                game.change_snake_direction(LEFT)
            if event.key == pg.K_RIGHT and game.get_snake_direction().x == 0:
                game.change_snake_direction(RIGHT)
            if event.key == pg.K_SPACE:
                game.on_space_pressed()

    # Draw all game objects
    game.draw()

    # Update the screen
    pg.display.update()
    # Maintain a frame rate of 60 frames per second
    clock.tick(60)

# Quit the game
pg.quit()

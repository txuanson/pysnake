"""
PySnake
Author: sxntrxn (tranxuanson2013@gmail.com)
"""

import pygame
from pygame.math import Vector2

from abc import ABC, abstractmethod
from random import randint
from pathlib import Path
from typing import Tuple

# Configuration screen
TOP_OFFSET = 150
HORIZONTAL_OFFSET = 50
BOT_OFFSET = 50

CELL_SIZE = 20
CELL_HORIZONTAL_COUNTONTAL_COUNT = 10
CELL_VERTICAL_COUNT = 10
WIDTH = CELL_HORIZONTAL_COUNTONTAL_COUNT * CELL_SIZE + 2 * HORIZONTAL_OFFSET
HEIGHT = CELL_VERTICAL_COUNT * CELL_SIZE + TOP_OFFSET + BOT_OFFSET

print(f"WIDTH: {WIDTH}, HEIGHT: {HEIGHT}")
print(
    f"CELL_HORIZONTAL_COUNTONTAL_COUNT: {CELL_HORIZONTAL_COUNTONTAL_COUNT}, CELL_VERTICAL_COUNT: {CELL_VERTICAL_COUNT}"
)

# Initialize the Pygame engine
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])
pygame.display.set_caption("PySnake")

# Set up clock
clock = pygame.time.Clock()


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
            # Temporary solution, in the future, we should tell the user that the game is over
            raise Exception("No valid position found for the food")


class GameObject(pygame.sprite.Sprite):
    @abstractmethod
    def draw(self):
        pass


class Snake(GameObject):
    body: list[Vector2] = [Vector2(0, 0), Vector2(1, 0), Vector2(2, 0)]
    direction = Vector2(1, 0)

    def __init__(self):
        super(Snake, self).__init__()

    def draw(self):
        for body_part in self.body:
            translated_pos = calculate_position(body_part.x, body_part.y)
            body_part_rect = pygame.rect.Rect(
                translated_pos[0], translated_pos[1], CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, (255, 255, 0), body_part_rect)

    def move(self):
        # Copy the body parts of the snake except the tail
        body_copy = self.body[1:]
        # Calculate the new head based on the current direction
        new_head = self.body[-1] + self.direction
        # Insert the new head at the last position
        body_copy.append(new_head)
        # Update the body
        self.body = body_copy[:]


class Food(GameObject):
    def __init__(self, snake_body: list[Vector2], size: int = 1):
        super(Food, self).__init__()
        self.pos = generate_food_position(snake_body, size)
        self.size = size

    def draw(self):
        translated_pos = calculate_position(self.pos.x, self.pos.y)
        food_rect = pygame.rect.Rect(
            translated_pos[0],
            translated_pos[1],
            CELL_SIZE * self.size,
            CELL_SIZE * self.size,
        )
        pygame.draw.rect(screen, (255, 0, 0), food_rect)

    def update(self, pos: Vector2):
        self.pos = pos


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body, 5)

    def tick(self):
        self.snake.move()
        if check_collision(
            self.snake.body[-1],
            self.food.pos,
            self.food.pos + Vector2(self.food.size, self.food.size),
        ):
            self.snake.body.insert(0, self.snake.body[0])
            self.food.update(generate_food_position(self.snake.body, self.food.size))

    def change_snake_direction(self, direction: Vector2):
        self.snake.direction = direction

    def get_snake_direction(self) -> Vector2:
        return self.snake.direction

    def draw(self):
        screen.fill((65, 152, 10))
        self.snake.draw()
        self.food.draw()


# Direction constants
MOVE_UP = Vector2(0, -1)
MOVE_DOWN = Vector2(0, 1)
MOVE_LEFT = Vector2(-1, 0)
MOVE_RIGHT = Vector2(1, 0)

# User events
GAME_TICK = pygame.USEREVENT
# Set the tickrate of the game
pygame.time.set_timer(GAME_TICK, 150)

game = Game()

# Run until the user asks to quit
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Move thticke everytick
        if event.type == GAME_TICK:
            game.tick()
        # Handle key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.get_snake_direction().y == 0:
                game.change_snake_direction(MOVE_UP)
            if event.key == pygame.K_DOWN and game.get_snake_direction().y == 0:
                game.change_snake_direction(MOVE_DOWN)
            if event.key == pygame.K_LEFT and game.get_snake_direction().x == 0:
                game.change_snake_direction(MOVE_LEFT)
            if event.key == pygame.K_RIGHT and game.get_snake_direction().x == 0:
                game.change_snake_direction(MOVE_RIGHT)

    # Draw all game objects
    game.draw()

    # Update the screen
    pygame.display.update()
    # Maintain a frame rate of 60 frames per second
    clock.tick(60)

# Quit the game
pygame.quit()

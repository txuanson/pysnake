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

# Set the width and height of the output window, in pixels
TOP_OFFSET = 150
HORIZONTAL_OFFSET = 50
BOT_OFFSET = 50

CELL_SIZE = 20
CELL_HORIZONTAL_COUNTONTAL_COUNT = 80
CELL_VERTICAL_COUNT = 20
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


class GameObject(pygame.sprite.Sprite):
    pos: Vector2

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self, pos_x: int, pos_y: int):
        pos = calculate_position(pos_x, pos_y)
        self.pos = Vector2(pos)


class Snake(GameObject):
    body: list[Vector2] = [Vector2(0, 0), Vector2(1, 0), Vector2(2, 0)]

    def __init__(self):
        super(Snake, self).__init__()
        pos = calculate_position(0, 3)
        self.pos = Vector2(pos)

    def draw(self):
        for body_part in self.body:
            translated_pos = calculate_position(body_part.x, body_part.y)
            body_part_rect = pygame.rect.Rect(
                translated_pos[0], translated_pos[1], CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(screen, (255, 255, 0), body_part_rect)


class Food(GameObject):
    def __init__(self, pos_x: int, pos_y: int, size: int = 1):
        super(Food, self).__init__()
        pos = calculate_position(pos_x, pos_y)
        self.pos = Vector2(pos)
        self.size = size

    def draw(self):
        food_rect = pygame.rect.Rect(
            self.pos.x, self.pos.y, CELL_SIZE * self.size, CELL_SIZE * self.size
        )
        pygame.draw.rect(screen, (255, 0, 0), food_rect)

    def update(self, pos_x: int, pos_y: int):
        # Disallow food to change position, for now
        pass


food = Food(2, 3, 1)
snake = Snake()

# Run until the user asks to quit
running = True
while running:

    # Did
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((65, 152, 10))

    # Draw the snake
    snake.draw()

    # Draw the food
    food.draw()

    # Update the screen
    pygame.display.update()
    # Maintain a frame rate of 60 frames per second
    clock.tick(60)

# Quit the game
pygame.quit()

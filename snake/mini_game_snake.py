import pygame
import random

pygame.init()
screen_color = (0, 255, 204)
snake_color = (0, 102, 2)
size = width, height = 1000, 600
count_blocks = 20
size_block = 27
otstup = 1
screen = pygame.display.set_mode(size)
screen.fill(screen_color)
pygame.display.flip()
pygame.display.set_caption('Змейка')
x1, y1 = random.randint(0, count_blocks), random.randint(0, count_blocks)


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y


snake_blocks = [Snake(x1, y1)]


def draw_block(color, y, x):
    pygame.draw.rect(screen, color, [200 + x * size_block + otstup * (x + 1),
                                     20 + y * size_block + otstup * (y + 1), size_block, size_block],
                     1)


def draw_snake(color, y, x):
    pygame.draw.rect(screen, color, [200 + x * size_block + otstup * (x + 1),
                                     20 + y * size_block + otstup * (y + 1), size_block, size_block],
                     0)


while True:
    screen.fill(screen_color)
    pygame.draw.rect(screen, (190, 190, 190), [10, 20, 160, 560])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    for y in range(count_blocks):
        for x in range(count_blocks):
            draw_block((255, 255, 255), y, x)
    for block in snake_blocks:
        draw_snake(snake_color, block.x, block.y)
    pygame.display.flip()

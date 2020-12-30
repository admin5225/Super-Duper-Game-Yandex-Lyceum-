import pygame
import random
import sys

pygame.init()
screen_color = (0, 255, 204)
snake_color = (0, 102, 2)
size = width, height = 1000, 600
count_blocks = 20
size_block = 27
otstup = 1
total = 0
text = pygame.font.SysFont('Times New Roman', 36)
screen = pygame.display.set_mode(size)
screen.fill(screen_color)
pygame.display.flip()
pygame.display.set_caption('Змейка')
x1, y1 = random.randint(0, count_blocks), random.randint(0, count_blocks)
clock = pygame.time.Clock()
fps = 2


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Snake) and self.x == other.x and self.y == other.y

    def check_crash(self):
        return 0 <= self.x < count_blocks and 0 <= self.y < count_blocks


snake_blocks = [Snake(9, 9), Snake(9, 10)]
apple = Snake(random.randint(0, count_blocks - 1), random.randint(0, count_blocks - 1))
dy = 0
dx = 1


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
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and dx != 0:
                dy = -1
                dx = 0
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dx != 0:
                dy = 1
                dx = 0
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dy != 0:
                dy = 0
                dx = 1
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dy != 0:
                dy = 0
                dx = -1
    screen_total = text.render(f'Счет: {total}', 0, (255, 255, 255))
    screen_speed = text.render(f'Турбо: {fps}', 0, (255, 255, 255))
    screen.blit(screen_total, (20, 20))
    screen.blit(screen_speed, (20, 50))
    for y in range(count_blocks):
        for x in range(count_blocks):
            draw_block((255, 255, 255), y, x)
    snakes_head = snake_blocks[-1]
    if not snakes_head.check_crash():
        pygame.quit()
        sys.exit()
    draw_snake((255, 0, 0), apple.x, apple.y)
    if apple == snakes_head:
        total += 1
        fps = total // 2 + fps
        snake_blocks.append(apple)
        apple = Snake(random.randint(0, count_blocks - 1), random.randint(0, count_blocks - 1))
        if apple in snake_blocks:
            apple = Snake(random.randint(0, count_blocks), random.randint(0, count_blocks))
    for block in snake_blocks:
        draw_snake(snake_color, block.x, block.y)
    new_head = Snake(snakes_head.x + dy, snakes_head.y + dx)
    snake_blocks.append(new_head)
    snake_blocks.pop(0)
    pygame.display.flip()
    clock.tick(fps)

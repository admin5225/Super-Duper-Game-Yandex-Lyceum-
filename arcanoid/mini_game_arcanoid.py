import os
import pygame
import sys
import random

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Арканойд")
total = 0
text = pygame.font.SysFont('Times New Roman', 24)
speed = 2
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data_arcanoid', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 60, 15)

    def update(self):
        pygame.draw.rect(screen, pygame.Color('#ffcc00'), (self.x, self.y, 60, 15))


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.w = 100
        self.h = 10

    def update(self):
        pygame.draw.rect(screen, (0, 0, 190), (self.x, self.y, self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.ball_x = 'left'
        self.ball_y = 'down'

    def update(self):
        if self.ball_x == "left":
            self.x -= speed
            if self.x < 10:
                self.ball_x = "right"
        if self.ball_y == 'down':
            self.y += speed
        if self.ball_y == 'up':
            self.y -= speed
            if self.y < 10:
                self.ball_y = 'down'
        if self.ball_x == "right":
            self.x += speed
            if self.x > width - 20:
                self.ball_x = "left"
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 10)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)


def collision():
    global total
    if ball.rect.colliderect(bar):
        ball.ball_y = "up"

    for n, brick in enumerate(bricks):
        if ball.rect.colliderect(brick):
            if ball.ball_y == "up":
                if ball.y == (brick.y + 20 - speed):
                    ball.ball_y = "down"
                else:
                    if ball.ball_x == "left":
                        ball.ball_x = "right"
                    else:
                        ball.ball_x = "left"
            else:
                if ball.y <= brick.y:
                    ball.ball_y = "up"
                else:
                    if ball.ball_x == "left":
                        ball.ball_x = "right"
                    else:
                        ball.ball_x = "left"
            bricks.pop(n)
            total += 1
            if bricks == []:
                pygame.quit()
                sys.exit()

    if ball.y > 570:
        pygame.quit()
        sys.exit()


def create_bricks():
    level = ''
    bricks = []
    h = 30
    w = 0
    n = 15
    for i in range(1, n * 8):
        if i % n == 0:
            level += '\t'
        level += str(random.randint(0, 1))
    level = level.split('\t')
    for line in level:
        for brick in line:
            if brick == "1":
                bricks.append(Brick(20 + w * 70, h))
            w += 1
            if w == n:
                w = 0
                h += 30
    return bricks


def show_bricks():
    for brick in bricks:
        brick.update()


if __name__ == '__main__':
    bar = Bar(width // 2 - 65, 550)
    ball = Ball(width // 2, height // 2)
    bricks = create_bricks()
    background = load_image('fon_truba.jpg')
    running = True
    while running:
        screen.blit(background, (0, 0))
        '''screen.fill((0, 0, 0))'''
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            left_move = True
            right_move = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            left_move = False
            right_move = True
        else:
            left_move = False
            right_move = False
        if left_move and bar.x > 5:
            bar.x -= 4
        if right_move and bar.x < width - 65:
            bar.x += 4
        ball.update()
        bar.update()
        collision()
        screen_total = text.render(f'Счет: {total}', 0, (255, 255, 255))
        screen.blit(screen_total, (width // 2 - 50, height - 30))
        show_bricks()
        pygame.display.update()

        clock.tick(120)

    pygame.quit()

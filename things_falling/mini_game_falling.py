import os
import sys

import pygame
import random

pygame.init()
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Falling things")
things_list = []
bombs = []
life = [1, 2, 3]
loosing_count = 0
total_count = 0
text = pygame.font.SysFont('Times New Roman', 24)
all_sprites = pygame.sprite.Group()
board = pygame.sprite.Sprite()
group_balls = pygame.sprite.Group()
group_bombs = pygame.sprite.Group()
group_board = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(group_balls, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        global loosing_count
        self.y += 1
        if self.y > height - 50:
            loosing_count += 1
            print(loosing_count)
            self.y = random.randrange(-50, -10)
            self.x = random.randrange(0, width - 5)
        '''pygame.draw.rect(screen, WHITE, (self.x, self.y, 10, 10))'''
        self.rect = pygame.Rect(self.x, self.y, 10, 10)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(group_bombs, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.y += 1
        if self.y > height - 50:
            self.y = random.randrange(-50, -10)
            self.x = random.randrange(0, width - 5)
        '''pygame.draw.circle(screen, RED, (self.x, self.y), 7)'''
        self.rect = pygame.Rect(self.x, self.y, 6, 6)


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(group_board, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.w = 100
        self.h = 10
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        '''pygame.draw.rect(screen, (0, 0, 190), (self.x, self.y, self.w, self.h))'''
        self.rect = pygame.Rect(self.x - 30, self.y, self.w, self.h)


def collision():
    global total_count
    for n, thing in enumerate(things_list):
        if thing.rect.colliderect(bar):
            total_count += 1
            things_list[n].kill()
            things_list.pop(n)
            print(len(things_list))
    for n, bomb in enumerate(bombs):
        if bomb.rect.colliderect(bar):
            bombs[n].kill()
            bombs.pop(n)
            if life:
                life.pop(-1)


if __name__ == '__main__':
    count_things = 20
    image_things = load_image('tree.png', -1)
    image_things = pygame.transform.scale(image_things, (50, 50))
    image_bomb = load_image('stone.png', -1)
    image_bomb = pygame.transform.scale(image_bomb, (30, 30))
    image_board = load_image('bag2.png', -1)
    image_board = pygame.transform.scale(image_board, (150, 60))
    image_life = load_image('heart.jpg', -1)
    image_life = pygame.transform.scale(image_life, (25, 25))
    background = load_image('background.gif')
    for i in range(count_things):
        x = random.randrange(0, width - 5)
        y = random.randrange(-350, 300)
        things_list.append(Ball(x, y, image_things))
        if i % 5 == 0:
            bombs.append(Bomb(random.randrange(0, width - 5), random.randrange(-350, 300), image_bomb))

    bar = Bar(width // 2 - 65, height - 50, image_board)
    running = True
    while running:
        '''screen.fill((213, 0, 0))'''
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not life:
                running = False
            if total_count == count_things:
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
            bar.x -= 6
        if right_move and bar.x < width - 100:
            bar.x += 6
        '''screen.fill(BLACK)'''

        for i in range(len(things_list)):
            Ball.update(things_list[i])

        for i in range(len(bombs)):
            Bomb.update(bombs[i])

        if loosing_count >= 10:
            life.pop(-1)
            loosing_count = 0

        bar.update()
        group_balls.draw(screen)
        group_bombs.draw(screen)
        group_board.draw(screen)

        collision()
        for i in life:
            life_rect = image_life.get_rect(center=((25 * i) - 10, 15))
            screen.blit(image_life, life_rect)
        screen_total = text.render(f'Счет: {total_count}', 0, (255, 255, 255))
        screen.blit(screen_total, (width - 85, 0))
        pygame.display.flip()
        clock.tick(90)
    pygame.quit()

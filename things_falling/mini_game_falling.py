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
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y

    def update(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 5)
        self.rect = pygame.Rect(self.x, self.y, 4, 4)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y

    def update(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 7)
        self.rect = pygame.Rect(self.x, self.y, 6, 6)


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


def collision():
    for n, brick in enumerate(things_list):
        if brick.rect.colliderect(bar):
            things_list.pop(n)
    for n, bomb in enumerate(bombs):
        if bomb.rect.colliderect(bar):
            bombs.pop(n)
            if life:
                life.pop(-1)


if __name__ == '__main__':
    for i in range(20):
        x = random.randrange(0, width - 5)
        y = random.randrange(-350, 300)
        things_list.append(Ball(x, y))
        if i % 5 == 0:
            bombs.append(Bomb(random.randrange(0, width - 5), random.randrange(-350, 300)))

    bar = Bar(width // 2 - 65, height - 50)
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not life:
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
        screen.fill(BLACK)

        for i in range(len(things_list)):
            Ball.update(things_list[i])
            things_list[i].y += 1

            if things_list[i].y > height - 50:
                loosing_count += 1
                print(loosing_count)
                y = random.randrange(-50, -10)
                things_list[i].y = y
                x = random.randrange(0, width - 5)
                things_list[i].x = x

        for i in range(len(bombs)):
            Bomb.update(bombs[i])
            bombs[i].y += 1

            if bombs[i].y > height - 50:
                y = random.randrange(-50, -10)
                bombs[i].y = y
                x = random.randrange(0, width - 5)
                bombs[i].x = x
        if loosing_count >= 10:
            life.pop(-1)
            loosing_count = 0

        for i in life:
            pygame.draw.rect(screen, RED, (20 * i, 580, 15, 15))

        bar.update()
        collision()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

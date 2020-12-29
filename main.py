import pygame

import os
import sys

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)


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


# Проверка на пересечение объекта с группой спрайтов (по маске)
def is_intersection(obj, group):
    intersection = False
    for el in group:
        if pygame.sprite.collide_mask(obj, el):
            if 120 <= (el.rect.y - obj.rect.y) <= 150:
                intersection = True

    return intersection


all_sprites = pygame.sprite.Group()
plates = pygame.sprite.Group()
groupDED = pygame.sprite.Group()
perses = pygame.sprite.Group()

# Картинка с платформой
plate_image = load_image('plate1.png')
# Картинки с персонажем
# pers_images = [load_image('dop_pers1.png'), load_image('dop_pers2.png')]

images = list()
for i in range(1, 35):
    images.append(load_image(f"ded{i}.png"))


class Plate(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(all_sprites, plates)

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Pers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, perses)

        self.count_image = 0
        self.image = pers_images[self.count_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count_image = 0

    def update(self):
        self.count_image = (self.count_image + 1) % 20
        if self.count_image % 10 == 0:
            self.image = pers_images[self.count_image // 10]


class DedMoroz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.moved = 1

        self.image = images[self.moved - 1]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.width = 150
        self.height = 150
        self.rect.x = x
        self.rect.y = y
        self.add(groupDED)

        self.jump = False
        # Начальная скорость прыжка
        self.speed_jump = 18
        self.jump_count = self.speed_jump
        self.step = 5

        # Начальная скорость падения
        self.speed_fall = 0

    def get_jump(self):
        # Проверка на возможность сделать прыжок
        if is_intersection(self, plates):
            self.jump = True
            self.jump_count = self.speed_jump

    def update(self):
        # Смена картинки
        if self.moved % 10 == 0:
            self.image = images[(self.moved - 1) // 10]
            self.mask = pygame.mask.from_surface(self.image)
        self.moved = (self.moved + 1) % 331

        # Проверка на пересечение с платформами и движение (влево, впараво)
        if left_move:
            self.rect.x -= self.step
        if right_move:
            self.rect.x += self.step

        if self.jump:
            if self.jump_count > 0:
                self.rect.y -= self.jump_count
                self.jump_count -= 1
            else:
                self.jump = False
                self.speed_fall = 0

        # Проверка на соприкосновение с платформами и падение
        if not is_intersection(self, plates):
            if not self.jump:
                self.rect.y += self.speed_fall
                self.speed_fall += 1
        else:
            self.speed_fall = 0

    def move_next(self):
        self.rect.x = 0
        self.rect.y = 430

    def move_back(self):
        self.rect.x = 950
        self.rect.y = 430


if __name__ == '__main__':
    screen.fill((255, 255, 255))

    ded = DedMoroz(10, 410)

    # Растягивание картинки платформы до нужной длины и её создание
    image = pygame.transform.scale(plate_image, (1000, 35))
    Plate(0, 560, image)
    image = pygame.transform.scale(plate_image, (200, 35))
    Plate(500, 400, image)
    Plate(600, 220, image)
    Plate(700, 80, image)
    # Pers(560, 290)

    clock = pygame.time.Clock()

    fons = [load_image('fon1.jpg'), load_image('fon2.jpg')]
    count = 1

    left_move, right_move, move = False, False, False

    running = True
    while running:
        screen.blit(fons[count - 1], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            left_move = True
            right_move = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            left_move = False
            right_move = True
        else:
            left_move = False
            right_move = False

        if ded.rect.x > 950:
            ded.move_next()
            count = (count + 1) % (len(fons) + 1)
            ded.rect.y = 410
            ded.jump = False
        if ded.rect.x < -30:
            ded.move_back()
            count = (count - 1) % (len(fons) + 1)
            ded.rect.y = 410
            ded.jump = False

        if not ded.jump:
            if keys[pygame.K_UP]:
                ded.get_jump()

        all_sprites.update()
        all_sprites.draw(screen)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

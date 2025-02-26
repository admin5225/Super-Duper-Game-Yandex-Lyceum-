import pygame

import os
import sys
import random

pygame.init()
pygame.display.set_caption('Подвиги Деда Мороза')
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


image_ico = load_image('ico.png')
pygame.display.set_icon(image_ico)


def final_game():
    k = 0
    text_final = pygame.font.SysFont('Times New Roman', 36)
    pygame.display.set_caption('Подвиги Деда Мороза')
    fon_final = load_image('final_fon.jpg')
    screen.blit(fon_final, (0, 0))
    image_win = load_image(os.path.join('pers5', 'win.png'))
    screen.blit(image_win, (0, 300))
    final_dialog = [load_image(os.path.join('final_dialog', '1.png')),
                    load_image(os.path.join('final_dialog', '2.png')),
                    load_image(os.path.join('final_dialog', '3.png')),
                    load_image(os.path.join('final_dialog', '4.png')),
                    load_image(os.path.join('final_dialog', '5.png')),
                    load_image(os.path.join('final_dialog', '6.png')),
                    load_image(os.path.join('final_dialog', '7.png')),
                    load_image(os.path.join('final_dialog', '8.png')),
                    load_image(os.path.join('final_dialog', '9.png'))]
    k = len(final_dialog) + 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if k == len(final_dialog) + 1:
                        screen.blit(fon_final, (0, 0))
                        k = 0
                    elif k != len(final_dialog):
                        screen.blit(final_dialog[k], (0, 300))
                        k += 1
                if event.key == pygame.K_q:
                    screen.fill((0, 0, 0))
                    text_for_final = text_final.render(f'Спасибо за игру!', 0, (255, 255, 255))
                    screen.blit(text_for_final, (width // 2 - 120, height // 2))

        pygame.display.flip()
        clock.tick(60)


# ------------------------------- Змейка -------------------------------------------------------------------------------
snake_color = (195, 200, 150)
screen_color = (0, 102, 2)
count_blocks = 20
size_block = 27
otstup = 1
total = 0
eating_apple = pygame.mixer.Sound(os.path.join('data', 'eating_apple.mp3'))
eating_snake = pygame.mixer.Sound(os.path.join('data', 'eating_snake.mp3'))
meeting_wall = pygame.mixer.Sound(os.path.join('data', 'meeting_with_wall.mp3'))
text = pygame.font.SysFont('Times New Roman', 36)

pers1_dialog = [load_image(os.path.join('pers1', '1.png')), load_image(os.path.join('pers1', '2.png')),
                load_image(os.path.join('pers1', '3.png')), load_image(os.path.join('pers1', '4.png')),
                load_image(os.path.join('pers1', '5.png')), load_image(os.path.join('pers1', '6.png')),
                load_image(os.path.join('pers1', '7.png')), load_image(os.path.join('pers1', '8.png'))]
pers1_win_image = load_image(os.path.join('pers1', 'win.png'))
pers1_lose_image = load_image(os.path.join('pers1', 'lose.png'))
pers1_return_game = load_image(os.path.join('pers1', 'return.png'))


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Snake) and self.x == other.x and self.y == other.y

    def check_crash(self):
        return 0 <= self.x < count_blocks and 0 <= self.y < count_blocks


def draw_block(color, y, x):
    pygame.draw.rect(screen, color, [200 + x * size_block + otstup * (x + 1),
                                     20 + y * size_block + otstup * (y + 1), size_block, size_block],
                     1)


def draw_snake(color, y, x):
    pygame.draw.rect(screen, color, [200 + x * size_block + otstup * (x + 1),
                                     20 + y * size_block + otstup * (y + 1), size_block, size_block],
                     0)


def snake():
    total = 0
    screen.fill(screen_color)
    pygame.display.set_caption('Мини игра - Змейка')
    x1, y1 = random.randint(0, count_blocks), random.randint(0, count_blocks)
    fps = 5

    snake_blocks = [Snake(9, 9), Snake(9, 10)]
    apple = Snake(random.randint(0, count_blocks - 1), random.randint(0, count_blocks - 1))
    dy = time_dy = 0
    dx = time_dx = 1
    flag = True

    while flag:
        screen.fill(screen_color)
        pygame.draw.rect(screen, (190, 190, 190), [10, 20, 160, 560])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and dx != 0:
                    time_dy = -1
                    time_dx = 0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dx != 0:
                    time_dy = 1
                    time_dx = 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dy != 0:
                    time_dy = 0
                    time_dx = 1
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dy != 0:
                    time_dy = 0
                    time_dx = -1
        screen_total = text.render(f'Счет: {total}', 0, (255, 255, 255))
        screen_speed = text.render(f'Турбо: {fps - 4}', 0, (255, 255, 255))
        screen.blit(screen_total, (20, 20))
        screen.blit(screen_speed, (20, 50))
        for y in range(count_blocks):
            for x in range(count_blocks):
                draw_block((255, 255, 255), y, x)
        snakes_head = snake_blocks[-1]
        if not snakes_head.check_crash():
            meeting_wall.play()
            break
        draw_snake((255, 0, 0), apple.x, apple.y)
        if apple == snakes_head:
            eating_apple.play()
            total += 1
            fps = total // 1 + 5
            snake_blocks.append(apple)
            apple = Snake(random.randint(0, count_blocks - 1), random.randint(0, count_blocks - 1))
            if apple in snake_blocks:
                apple = Snake(random.randint(0, count_blocks), random.randint(0, count_blocks))
        for block in snake_blocks:
            draw_snake(snake_color, block.x, block.y)
        pygame.display.flip()
        dx, dy = time_dx, time_dy
        new_head = Snake(snakes_head.x + dy, snakes_head.y + dx)
        if new_head in snake_blocks:
            eating_snake.play()
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        clock.tick(fps)

    if total >= 7:
        fons.append(fon_level_1)
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------------

# -------------------------------Собирание веток------------------------------------------------------------------------

pers2_dialog = []
for i in range(16):
    pers2_dialog.append(load_image(os.path.join('pers2', f"{i + 1}.png")))

pers2_win_image = load_image(os.path.join('pers2', 'win.png'))
pers2_lose_image = load_image(os.path.join('pers2', 'lose.png'))
pers2_return_game = load_image(os.path.join('pers2', 'return.png'))

gift_image = pygame.transform.scale(load_image(os.path.join('gifts', 'gift2.png')), (50, 50))
number_image = pygame.transform.scale(load_image(os.path.join('gifts', 'number.png')), (50, 30))
lose_heart = pygame.mixer.Sound(os.path.join('data', 'lose_heart.mp3'))
get_tree = pygame.mixer.Sound(os.path.join('data', 'get_tree.mp3'))
get_stone = pygame.mixer.Sound(os.path.join('data', 'get_stone.mp3'))
all_sprites = pygame.sprite.Group()
board = pygame.sprite.Sprite()
group_things = pygame.sprite.Group()
group_bombs = pygame.sprite.Group()
group_board = pygame.sprite.Group()
clock = pygame.time.Clock()
loosing_count = 0
things_list = []
bombs = []
total_count = 0
life = [1, 2, 3]


class Thing(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(group_things, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.loosing_count = 0
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        global loosing_count
        self.y += 1
        if self.y > height - 50:
            loosing_count += 1
            '''print(loosing_count)'''
            self.y = random.randrange(-50, -10)
            self.x = random.randrange(0, width - 5)
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
        self.rect = pygame.Rect(self.x - 30, self.y, self.w, self.h)


def collision_falling(bar):
    global loosing_count, things_list, bombs, total_count, life
    for n, thing in enumerate(things_list):
        if thing.rect.colliderect(bar):
            total_count += 1
            things_list[n].kill()
            things_list.pop(n)
            get_tree.play()
            '''print(len(things_list))'''
    for n, bomb in enumerate(bombs):
        if bomb.rect.colliderect(bar):
            bombs[n].kill()
            bombs.pop(n)
            get_stone.play()
            if life:
                lose_heart.play()
                life.pop(-1)
    return total_count


def falling_things():
    global loosing_count, things_list, bombs, total_count, life
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Ловим ветки, а камни пропускаем")
    text = pygame.font.SysFont('Times New Roman', 24)
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
    bar = Bar(width // 2 - 65, height - 50, image_board)
    for i in range(count_things):
        x = random.randrange(0, width - 5)
        y = random.randrange(-350, 300)
        '''print(x)
        print(y)
        print(image_things)'''
        things_list.append(Thing(x, y, image_things))
        if i % 5 == 0:
            bombs.append(Bomb(random.randrange(0, width - 5), random.randrange(-350, 300), image_bomb))

    running = True
    while running:
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

        if not life:
            break
        if total_count == count_things:
            break

        for i in range(len(things_list)):
            Thing.update(things_list[i])

        for i in range(len(bombs)):
            Bomb.update(bombs[i])

        if loosing_count >= 10:
            lose_heart.play()
            life.pop(-1)
            loosing_count = 0

        bar.update()
        group_things.draw(screen)
        group_bombs.draw(screen)
        group_board.draw(screen)

        collision_falling(bar)
        for i in life:
            life_rect = image_life.get_rect(center=((25 * i) - 10, 15))
            screen.blit(image_life, life_rect)
        screen_total = text.render(f'Счет: {total_count}', 0, (255, 255, 255))
        screen.blit(screen_total, (width - 85, 0))
        pygame.display.flip()
        clock.tick(90)
    if total_count == count_things:
        global pers3
        pers3 = Pers(780, 169, pers3_dialog, pers3_win_image, None, None, pers3_pass_game, perses_level_2)

        return True
    else:
        bar.kill()
        for i in bombs:
            i.kill()
        for i in things_list:
            i.kill()
        screen.blit(background, (0, 0))
        loosing_count = 0
        things_list = []
        bombs = []
        total_count = 0
        life = [1, 2, 3]
        count_things = 20
        return False


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------- Арканойд--------------------------------------------------------------------
pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
get_bricks = pygame.mixer.Sound(os.path.join('data', 'bricks.mp3'))
get_ball_jump = pygame.mixer.Sound(os.path.join('data', 'lol.mp3'))
total_arkanoid = 0
text_arkanoid = pygame.font.SysFont('Times New Roman', 24)
speed = 2
clock = pygame.time.Clock()
all_sprites_arkanoid = pygame.sprite.Group()
bricks_sprite = pygame.sprite.Group()
background = load_image('fon_truba.jpg')
error_game = False
bricks = []


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(bricks_sprite)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 60, 15)

    def update(self):
        pygame.draw.rect(screen, pygame.Color('#ffcc00'), (self.x, self.y, 60, 15))


class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_arkanoid)
        self.x = x
        self.y = y
        self.w = 100
        self.h = 10

    def update(self):
        pygame.draw.rect(screen, (0, 0, 190), (self.x, self.y, self.w, self.h))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_arkanoid)
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


bar = player(width // 2 - 65, 550)
ball = Ball(width // 2, height // 2)


def collision():
    global total_arkanoid, bricks, error_game
    if ball.rect.colliderect(bar):
        get_ball_jump.play()
        ball.ball_y = "up"

    for n, brick in enumerate(bricks):
        if ball.rect.colliderect(brick):
            get_ball_jump.play()
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
            get_bricks.play()
            bricks.pop(n)
            brick.kill()
            total_arkanoid += 1

    if ball.y > 570:
        error_game = True


def create_bricks():
    global bricks
    level = ''
    bricks = []
    h = 30
    w = 0
    n = 14
    for i in range(1, n * 7):
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
    '''print(len(bricks))'''
    return bricks


def show_bricks():
    for brick in bricks:
        brick.update()


def arkanoid():
    global bricks, error_game, total_arkanoid
    pygame.display.set_caption("Арканойд")
    first_briks = create_bricks()
    len_first_briks = len(first_briks)
    running = True
    while running:
        screen.blit(background, (0, 0))
        '''screen.fill((0, 0, 0))'''
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            left_move = True
            right_move = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            left_move = False
            right_move = True
        elif keys[pygame.K_z]:
            total_arkanoid = len_first_briks
        else:
            left_move = False
            right_move = False
        if left_move and bar.x > 5:
            bar.x -= 4
        if right_move and bar.x < width - 100:
            bar.x += 4
        ball.update()
        bar.update()
        collision()
        '''print(len(bricks_sprite))'''
        screen_total_arkanoid = text_arkanoid.render(f'Счет: {total_arkanoid}', 0, (255, 255, 255))
        screen.blit(screen_total_arkanoid, (width // 2 - 50, height - 30))
        show_bricks()
        pygame.display.update()

        clock.tick(120)
        if error_game:
            total_arkanoid = 0
            bar.kill()
            ball.x = width // 2
            ball.y = height // 2
            ball.kill()
            error_game = False
            for n, brick in enumerate(bricks):
                brick.kill()
                bricks.pop(n)
            for n, brick in enumerate(first_briks):
                brick.kill()
                bricks.pop(n)
            '''print(all_sprites_arkanoid)'''
            for i in all_sprites_arkanoid:
                i.kill()
            for i in bricks_sprite:
                i.kill()
            '''print(all_sprites_arkanoid)'''
            return False
        if total_arkanoid == len_first_briks or len(bricks_sprite) == 0:
            bar.kill()
            ball.kill()
            '''print(total_arkanoid)
            print(bricks)'''
            for n, brick in enumerate(bricks):
                brick.kill()
                bricks.pop(n)
            for n, brick in enumerate(first_briks):
                brick.kill()
                bricks.pop(n)
            for i in all_sprites_arkanoid:
                i.kill()
            for i in bricks_sprite:
                i.kill()
            final_game()
            return True

    pygame.quit()


# ----------------------------------------- Подарки---------------------------------------------------------------------

pers3_dialog = []
for i in range(7):
    pers3_dialog.append(load_image(os.path.join('pers3', f"{i + 1}.png")))
pers3_win_image = load_image(os.path.join('pers3', 'win.png'))

gift_image = pygame.transform.scale(load_image(os.path.join('gifts', 'gift2.png')), (50, 50))
number_image = pygame.transform.scale(load_image(os.path.join('gifts', 'number.png')), (50, 30))

pers4_dialog = []
for i in range(8):
    pers4_dialog.append(load_image(os.path.join('pers4', f"{i + 1}.png")))
pers4_win_image = load_image(os.path.join('pers4', "win.png"))


# Указываются координаты и группа уровня
class Gift(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group, all_sprites)

        self.image = gift_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.direction_move = -1
        self.move_count = 0
        self.delete = False

    def update(self):
        if self.delete:
            if self.move_count == 20:
                self.kill()
            else:
                self.rect.y -= 2
                self.move_count += 1
                screen.blit(number_image, (self.rect.x - 50, self.rect.y + 10))
        else:
            if self.move_count == 40:
                self.direction_move = -self.direction_move
                self.move_count = 0
            if self.move_count % 2 == 0:
                self.rect.y += self.direction_move
            self.move_count += 1

    def destroy(self):
        self.delete = True
        self.move_count = 0


def pers3_pass_game():
    fons.append(fon_level_1)
    return True


def gifts():
    Gift(280, 450, gifts_level_1)
    Gift(210, 450, gifts_level_1)
    Gift(350, 450, gifts_level_1)
    Gift(610, 450, gifts_level_1)
    Gift(680, 450, gifts_level_1)
    Gift(750, 450, gifts_level_1)
    Gift(410, 250, gifts_level_1)
    Gift(480, 250, gifts_level_1)
    Gift(550, 250, gifts_level_1)
    Gift(600, 520, gifts_level_2)
    Gift(670, 520, gifts_level_2)
    Gift(530, 520, gifts_level_2)
    Gift(460, 520, gifts_level_2)
    Gift(740, 520, gifts_level_2)
    Gift(590, 295, gifts_level_2)
    Gift(660, 295, gifts_level_2)
    Gift(730, 295, gifts_level_2)
    Gift(470, 80, gifts_level_2)
    Gift(540, 80, gifts_level_2)
    Gift(610, 80, gifts_level_2)
    Gift(400, 80, gifts_level_2)
    Gift(330, 80, gifts_level_2)
    Gift(260, 80, gifts_level_2)
    Gift(190, 80, gifts_level_2)
    Gift(260, 150, gifts_level_2)
    Gift(190, 150, gifts_level_2)
    Gift(410, 230, gifts_level_3)
    Gift(480, 230, gifts_level_3)
    Gift(550, 230, gifts_level_3)
    Gift(210, 200, gifts_level_3)

    ded.collect_gifts = True
    pers3.kill()
    pers4.kill()
    return True


# ----------------------------------------------------------------------------------------------------------------------

# ------------------------------------------- Аракноид -----------------------------------------------------------------
pers5_dialog = []
for i in range(9):
    pers5_dialog.append(load_image(os.path.join('pers5', f"{i + 1}.png")))
pers5_win_image = load_image(os.path.join('pers5', 'win.png'))
pers5_lose_image = load_image(os.path.join('pers5', 'lose.png'))
pers5_return_game = load_image(os.path.join('pers5', 'return.png'))


# ----------------------------------------------------------------------------------------------------------------------
# Выводится одна картинка до нажатия
def one_image(image):
    flag = True
    while flag:
        screen.blit(image, (0, 300))

        for event in pygame.event.get():
            pas = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if pas[pygame.K_e]:
                    key = 'E'
                    flag = False
                if pas[pygame.K_q]:
                    key = 'Q'
                    flag = False

        pygame.display.flip()
    return key


# Взаимодействие
def interaction(pers, game, dialog_images, win_image, lose_image, return_image):
    dialog_image_count = 0
    is_dialog = True
    start_game = True

    if pers.active_dialog:
        while is_dialog:
            screen.blit(dialog_images[dialog_image_count], (0, 300))

            for event in pygame.event.get():
                pas = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if pas[pygame.K_e]:
                        if (dialog_image_count + 1) == len(dialog_images):
                            is_dialog = False
                        else:
                            dialog_image_count += 1
                    elif pas[pygame.K_q]:
                        is_dialog = False
                        start_game = False
            pygame.display.flip()
    else:
        one_image(return_image)

    if start_game:
        pers.active_dialog = False

        exit = False
        while True:
            is_win = game()

            if is_win:
                one_image(win_image)
                exit = True
            else:
                key = one_image(lose_image)
                if key == 'Q':
                    exit = True
                    pygame.display.set_caption('Подвиги Деда Мороза')
            if exit:
                pygame.display.set_caption('Подвиги Деда Мороза')
                return is_win


# Проверка на пересечение объекта с группой спрайтов (по маске)
def is_intersection(obj, group):
    intersection_plate = False
    intersection_pers = False

    for el in group:
        if pygame.sprite.collide_mask(obj, el):
            if 110 <= (el.rect.y - obj.rect.y) <= 150:
                intersection_plate = True
            else:
                intersection_pers = True

    return intersection_plate, intersection_pers


class Plate(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        super().__init__(group, all_sprites)

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Pers(pygame.sprite.Sprite):
    def __init__(self, x, y, dialog_images, win_image, lose_image, return_image, game, group):
        super().__init__(group, all_sprites)

        self.count_image = 0
        self.images = pers_images
        self.image = self.images[self.count_image]
        self.mask = pygame.mask.from_surface(self.image)

        self.dialog_images = dialog_images
        self.win_image = win_image
        self.lose_image = lose_image
        self.return_image = return_image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.game = game
        # Флаг активности задания и диалога
        self.active_game = True
        self.active_dialog = True

    def update(self):
        self.count_image = (self.count_image + 1) % 20
        if self.count_image % 10 == 0:
            self.image = self.images[self.count_image // 10]

    def start_game(self):
        win = interaction(self, self.game, self.dialog_images, self.win_image, self.lose_image, self.return_image)

        if win:
            self.active_game = False
            self.count_image = 0
            self.images = active_pers_images


class DedMoroz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(groupDED, all_sprites)

        self.count_image = 1

        self.image = images_ded_AFK[self.count_image - 1]
        self.images = images_ded_AFK
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.collect_gifts = False

        self.width = 150
        self.height = 150
        self.rect.x = x
        self.rect.y = y

        self.jump = False
        # Начальная скорость прыжка
        self.speed_jump = 18
        self.jump_count = self.speed_jump
        self.step = 5

        # Начальная скорость падения
        self.speed_fall = 0

    def get_jump(self):
        # Проверка на возможность сделать прыжок
        if is_intersection(self, groups_plates[level_count - 1])[0]:
            self.jump = True
            self.jump_count = self.speed_jump

    def get_images(self, images):
        if self.images != images:
            self.images = images
            self.count_image = 1
            self.rect.y -= 5

    def update(self):
        # Смена картинки
        if self.count_image % 10 == 0:
            self.image = self.images[((self.count_image // 10) - 1)]
            self.mask = pygame.mask.from_surface(self.image)
        self.count_image = (self.count_image + 1) % ((len(self.images) * 10) + 1)

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
        if not is_intersection(self, groups_plates[level_count - 1])[0]:
            if not self.jump:
                self.rect.y += self.speed_fall
                self.speed_fall += 1
        else:
            self.speed_fall = 0

    def move_next(self):
        self.rect.x = 0

    def move_back(self):
        self.rect.x = 890


def check_move(is_prolog=False):
    global left_move, right_move

    keys = pygame.key.get_pressed()

    # Передвижение деда
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        left_move = True
        right_move = False
        ded.get_images(images_ded_move_left)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        left_move = False
        right_move = True
        ded.get_images(images_ded_move_right)
    else:
        left_move = False
        right_move = False
        ded.get_images(images_ded_AFK)

    # Прыжок
    if not ded.jump:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ded.get_jump()

    if is_prolog:
        if ded.rect.x < -20:
            left_move = False


def prolog():
    global prolog_fon_count, prolog_fon_image

    text1 = font.render(f"Передвижение:", True, (0, 0, 128))
    text2 = font.render(f"<--    -->", True, (0, 0, 128))
    text3 = font.render(f"или", True, (0, 0, 128))
    text4 = font.render(f"A        D", True, (0, 0, 128))
    text5 = font.render(f"Прыжок", True, (0, 0, 128))
    text6 = font.render(f"W  или  ^", True, (0, 0, 128))
    text7 = font.render(f"перепрыгните через яму", True, (0, 0, 128))

    print_text2 = False
    run = True
    while run:
        screen.blit(prolog_fon_image, (0, 0))
        if prolog_fon_count % 5 == 0:
            prolog_fon_image = prolog_fons[(prolog_fon_count // 5) - 1]
        prolog_fon_count = (prolog_fon_count + 1) % (len(prolog_fons) * 5)

        if ded.rect.x >= 440:
            print_text2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not is_intersection(ded, prolog_plates)[0]:
            ded.rect.y += 10

        if ded.rect.y > 10000:
            sound_fail.play()
            run = False

        check_move(True)

        groupDED.update()
        groupDED.draw(screen)
        prolog_plates.draw(screen)

        screen.blit(text1, (100, 250))
        screen.blit(text2, (135, 275))
        screen.blit(text3, (155, 300))
        screen.blit(text4, (135, 325))

        if print_text2:
            screen.blit(text5, (450, 250))
            screen.blit(text6, (450, 300))
            screen.blit(text7, (550, 370))

        clock.tick(60)
        pygame.display.flip()

    text5_font = pygame.font.Font(None, 80)
    text5 = text5_font.render(f"Прошло 5 часов...", True, (0, 0, 128))
    count = 0
    zvon.play()
    while count < 26000:
        screen.fill((255, 255, 255))
        if count > 10850:
            screen.blit(text5, (250, 200))
        count += 1

        pygame.display.flip()
    ded.kill()


if __name__ == '__main__':
    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 36)

    # Звуки
    get_gift = pygame.mixer.Sound(os.path.join('data', 'get_gift.mp3'))
    sound_fail = pygame.mixer.Sound(os.path.join('data', 'fail.mp3'))
    zvon = pygame.mixer.Sound(os.path.join('data', 'zvon.mp3'))

    # Создание групп
    all_sprites = pygame.sprite.Group()
    perses_level_1 = pygame.sprite.Group()
    perses_level_2 = pygame.sprite.Group()
    perses_level_3 = pygame.sprite.Group()
    perses_level_4 = pygame.sprite.Group()
    plates_level_1 = pygame.sprite.Group()
    plates_level_2 = pygame.sprite.Group()
    plates_level_3 = pygame.sprite.Group()
    plates_level_4 = pygame.sprite.Group()
    gifts_level_1 = pygame.sprite.Group()
    gifts_level_2 = pygame.sprite.Group()
    gifts_level_3 = pygame.sprite.Group()
    gifts_level_4 = pygame.sprite.Group()
    groupDED = pygame.sprite.Group()

    # Картинка с платформой
    plate1_image = load_image('plate1.png')
    plate2_image = load_image('plate2.png')
    # Картинки с персонажем
    pers_images = [load_image('dop_pers1.png'), load_image('dop_pers2.png')]
    active_pers_images = [load_image('dop_pers_active1.png'), load_image('dop_pers_active2.png')]

    # Анимация деда АФК
    images_ded_AFK = list()
    for i in range(1, 35):
        images_ded_AFK.append(load_image(f"ded{i}.png"))

    # Анимация деда при движении
    images_ded_move_right = [load_image(os.path.join('movement', 'ded1.png')),
                             load_image(os.path.join('movement', 'ded2.png')),
                             load_image(os.path.join('movement', 'ded3.png')),
                             load_image(os.path.join('movement', 'ded4.png')),
                             load_image(os.path.join('movement', 'ded5.png'))]

    images_ded_move_left = []
    for el in images_ded_move_right:
        images_ded_move_left.append(pygame.transform.flip(el, True, False))

    ded = DedMoroz(10, 410)

    # Растягивание картинки платформы до нужной длины и её создание
    big_plate = pygame.transform.scale(plate2_image, (1010, 40))
    prolog_plate = pygame.transform.scale(plate2_image, (600, 40))
    Plate(0, 570, big_plate, plates_level_1)
    Plate(0, 570, big_plate, plates_level_2)
    Plate(0, 570, big_plate, plates_level_3)
    Plate(0, 570, big_plate, plates_level_4)
    plate_image = pygame.transform.scale(plate1_image, (200, 35))

    # Уровень 1
    Plate(10, 200, plate_image, plates_level_1)
    Plate(50, 200, plate_image, plates_level_1)
    Plate(200, 500, plate_image, plates_level_1)
    Plate(600, 500, plate_image, plates_level_1)
    Plate(810, 350, plate_image, plates_level_1)
    Plate(600, 200, plate_image, plates_level_1)
    Plate(400, 300, plate_image, plates_level_1)
    Pers(-20, 90, pers1_dialog, pers1_win_image, pers1_lose_image, pers1_return_game, snake, perses_level_1)

    # Уровень 2
    little_plate = pygame.transform.scale(plate1_image, (50, 35))
    Plate(-5, 350, plate_image, plates_level_2)
    Plate(400, 330, little_plate, plates_level_2)
    Plate(580, 345, plate_image, plates_level_2)
    Plate(800, 280, plate_image, plates_level_2)
    Plate(460, 130, plate_image, plates_level_2)
    Pers(150, 459, pers2_dialog, pers2_win_image, pers2_lose_image, pers2_return_game, falling_things, perses_level_2)

    # Уровень 3
    Plate(200, 250, plate_image, plates_level_3)
    Plate(400, 280, plate_image, plates_level_3)
    Plate(600, 250, plate_image, plates_level_3)
    pers4 = Pers(600, 140, pers4_dialog, pers4_win_image, None, None, gifts, perses_level_3)

    # Уровень 4
    Plate(50, 500, plate_image, plates_level_4)
    Plate(200, 400, plate_image, plates_level_4)
    Plate(50, 250, plate_image, plates_level_4)
    Plate(500, 200, plate_image, plates_level_4)
    Plate(450, 200, plate_image, plates_level_4)
    Plate(630, 150, plate_image, plates_level_4)
    Pers(630, 40, pers5_dialog, pers5_win_image, pers5_lose_image, pers5_return_game, arkanoid, perses_level_4)

    clock = pygame.time.Clock()

    # Фоны
    fon_level_1 = []
    for i in range(150):
        image = load_image(os.path.join('background', os.path.join('level1', f'fon{i + 1}.png')))
        fon_level_1.append(pygame.transform.scale(image, (1000, 600)))
    fon_level_2 = []
    for i in range(52):
        image = load_image(os.path.join('background', os.path.join('level2', f'fon{i + 1}.png')))
        fon_level_2.append(pygame.transform.scale(image, (1000, 600)))
    house_image = load_image(os.path.join('background', 'house.png'))

    # Группы для смены локаций
    groups_perses = [perses_level_1, perses_level_2, perses_level_3, perses_level_4]
    groups_plates = [plates_level_1, plates_level_2, plates_level_3, plates_level_4]
    groups_gifts = [gifts_level_1, gifts_level_2, gifts_level_3, gifts_level_4]
    fons = [fon_level_1]
    '''fons = [fon_level_1, fon_level_1, fon_level_1, fon_level_1]'''
    fon_count = 4
    level_count = 1
    fon_image = fons[level_count - 1][fon_count - 1]
    left_move, right_move, move = False, False, False
    kol_gifts = 0

    # Пролог
    prolog_plates = pygame.sprite.Group()
    prolog_fons = fon_level_2
    prolog_fon_count = 1
    prolog_fon_image = prolog_fons[prolog_fon_count]
    ded.step = 2

    Plate(0, 570, prolog_plate, prolog_plates)
    Plate(800, 570, prolog_plate, prolog_plates)

    prolog()

    ded = DedMoroz(10, 410)
    ded.step = 5
    # Основная игра
    screen.blit(fon_image, (0, 0))
    one_image(load_image('ded_replic1.png'))
    running = True
    while running:
        screen.blit(fon_image, (0, 0))
        if fon_count % 5 == 0:
            fon_image = fons[level_count - 1][(fon_count // 5) - 1]
        fon_count = (fon_count + 1) % (len(fons[level_count - 1]) * 5)
        if level_count == 4:
            screen.blit(house_image, (400, 170))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        check_move()

        # Переход на соседние карты
        if ded.rect.x > 895:
            if level_count + 1 <= len(fons):
                ded.move_next()
                level_count = (level_count + 1) % (len(fons) + 1)
                fon_count = 10
            else:
                right_move = False
        if ded.rect.x < -20:
            if level_count - 1 > 0:
                ded.move_back()
                level_count = (level_count - 1) % (len(fons) + 1)
                fon_count = 10
            else:
                left_move = False
        if ded.rect.y > 880:
            ded.rect.y -= 30

        # Если провалился
        if ded.rect.y > 570:
            ded.rect.y = 410

        # Взаимодействие с персонажами
        if is_intersection(ded, groups_perses[level_count - 1])[1]:
            if keys[pygame.K_e]:
                pers = pygame.sprite.spritecollideany(ded, groups_perses[level_count - 1])
                if pers.active_game:
                    pers.start_game()

        # Собирание подарков (одно из заданий)
        if ded.collect_gifts:
            if kol_gifts == 30:
                ded.collect_gifts = False
                fons.append(fon_level_1)

            if is_intersection(ded, groups_gifts[level_count - 1])[1]:
                gift = pygame.sprite.spritecollideany(ded, groups_gifts[level_count - 1])
                if not gift.delete:
                    kol_gifts += 1
                    get_gift.play()
                    gift.destroy()
            text = font.render(f"Подарков собрано: {kol_gifts}", True, (255, 20, 147))
            screen.blit(text, (350, 25))

        all_sprites.update()
        groupDED.draw(screen)
        groups_perses[level_count - 1].draw(screen)
        groups_plates[level_count - 1].draw(screen)
        groups_gifts[level_count - 1].draw(screen)

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

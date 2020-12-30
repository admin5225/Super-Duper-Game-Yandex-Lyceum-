import pygame

pygame.init()
snake_color = (0, 255, 204)
size = width, height = 1000, 600
count_blocks = 20
size_block = 27
otstup = 1
screen = pygame.display.set_mode(size)
screen.fill(snake_color)
pygame.display.flip()
pygame.display.set_caption('Змейка')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill(snake_color)
    for y in range(count_blocks):
        for x in range(count_blocks):
            pygame.draw.rect(screen, (255, 255, 255), [200 + x * size_block + otstup * (x + 1),
                                                       20 + y * size_block + otstup * (y + 1), size_block, size_block], 1)

    pygame.display.flip()

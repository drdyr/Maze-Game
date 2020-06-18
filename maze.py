import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(100, 100))

    def update(self):
        pass


class Maze():
    def __init__(self, width, height):
        for x in range(width):
            for y in range(height):
                rect = pygame.Rect((screen_width / width) * x, (screen_height / height) * y, screen_width / width, screen_height / height)
                pygame.draw.rect(screen, (200, 200, 200), rect, 0)

class Cell():
    def __init(self, x, y, type):
        self.x = x
        self.y = y
        self.type = WALL

PASSAGE = 1
WALL = 0

player1 = Player()
player_group = pygame.sprite.Group()
player_group.add(player1)

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    player_group.draw(screen)
    player_group.update()
    maze = Maze(25, 25)
    pygame.display.flip()
    clock.tick(60)

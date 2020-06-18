import random
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


class Maze:
    def __init__(self, width, height):
        self.cells = []
        self.odd_cells = []
        self.width = width
        self.height = height
        for x in range(width):
            for y in range(height):
                cell = Cell(x, y, WALL, (screen_width / width), (screen_height / height))
                if (x != 0 and x != width - 1) and (y != 0 and y != height - 1):
                    self.cells.append(cell)
                    if x % 2 == 1 and y % 2 == 1:
                        self.odd_cells.append(cell)

    def generate(self):
        cells = self.odd_cells
        stack = []
        start_cell = random.choice(cells)
        stack.append(start_cell)
        while len(stack) != 0:
            neighbour = random.choice(get_neighbours(start_cell))

    def get_neighbours(self, cell):
        x = cell.x
        y = cell.y
        neighbours = []
        for i in range(-2, 2, 4):
            # add is unvisited
            if Cell(x + i, y, WALL, (screen_width / self.width), (screen_height / self.height)) in self.odd_cells:
                neighbours.append(Cell(x + i, y, WALL, (screen_width / self.width), (screen_height / self.height)))
            if Cell(x, y + i, WALL, (screen_width / self.width), (screen_height / self.height)) in self.odd_cells:
                neighbours.append(Cell(x, y + i, WALL, (screen_width / self.width), (screen_height / self.height)))

        return neighbours


class Cell:
    def __init__(self, x, y, cell_type, width, height):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        self.rect = pygame.Rect(width * x, height * y, width,
                                height)
        pygame.draw.rect(screen, cell_type, self.rect, 0)

    def set_type(self, cell_type):
        self.cell_type = cell_type
        pygame.draw.rect(screen, cell_type, self.rect, 0)


PASSAGE = (255, 255, 255)
WALL = (170, 170, 170)

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

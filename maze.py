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
        self.cell_width = screen_width / width
        self.cell_height = screen_height / height
        for x in range(width):
            for y in range(height):
                cell = Cell(x, y, self)
                cell.set_type(WALL)
                if (x != 0 and x != width - 1) and (y != 0 and y != height - 1):
                    self.cells.append(cell)
                    if x % 2 == 1 and y % 2 == 1:
                        self.odd_cells.append(cell)
                        cell.set_type(PASSAGE)

    def generate(self):
        cells = self.odd_cells
        stack = []
        current_cell = random.choice(cells)
        stack.append(current_cell)
        while len(stack) != 0:
            neighbour = random.choice(self.get_neighbours(current_cell))
            wall = Cell((neighbour.x + current_cell.x) / 2, (neighbour.y + current_cell.y) / 2, self)
            wall.set_type(PASSAGE)
            current_cell = neighbour
            stack.append(current_cell)
            while len(self.get_neighbours(current_cell)) == 0 and len(stack) != 0:
                current_cell = stack.pop()

    def get_neighbours(self, cell):
        x = cell.x
        y = cell.y
        neighbours = []
        for i in range(-2, 2, 4):
            cell1 = Cell(x + i, y, self)
            cell2 = Cell(x, y + i, self)
            if cell1 in self.odd_cells and self.unvisited(cell1):
                print("adding")
                neighbours.append(Cell(x + i, y, self))
            if cell2 in self.odd_cells and self.unvisited(cell2):
                print("adding")
                neighbours.append(Cell(x, y + i, self))

        return neighbours

    def unvisited(self, cell):
        x = cell.x
        y = cell.y
        if (self.get_cell_type(x + 1, y) == WALL and
                self.get_cell_type(x - 1, y) == WALL and
                self.get_cell_type(x, y + 1) == WALL and
                self.get_cell_type(x, y - 1) == WALL):
            print("unvisited")
            return True
        else:
            return False

    def get_cell_type(self, x, y):
        if Cell(x, y, self) in self.cells:
            index = self.cells.index(Cell(x, y, maze))
            return self.cells[index].get_type()


class Cell:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(maze.cell_width * self.x, maze.cell_height * self.y, maze.cell_width,
                                maze.cell_height)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        pygame.draw.rect(screen, self.cell_type, self.rect, 0)

    def set_type(self, cell_type):
        self.cell_type = cell_type
        self.draw()

    def get_type(self):
        return self.cell_type


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
    maze = Maze(11, 11)
    maze.generate()
    pygame.display.flip()
    clock.tick(60)

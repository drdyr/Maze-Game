import random
import pygame
import sys


class Maze:
    def __init__(self, width, height):
        self.cells = []
        self.odd_cells = []
        self.width = width
        self.height = height
        self.cell_side_length = cell_side_length

        for x in range(width):
            for y in range(height):
                cell = Cell(x, y, self)
                if x % 2 == 1 and y % 2 == 1 and x != 0 and x != width - 1 and y != 0 and y != height - 1:
                    cell.set_type(PASSAGE)
                    self.odd_cells.append(cell)
                self.cells.append(cell)

    def draw(self):
        for cell in self.cells:
            cell.draw()

    def generate(self):
        cells = self.odd_cells
        stack = []
        current_cell = random.choice(cells)
        stack.append(current_cell)
        while len(stack) != 0:
            neighbour = random.choice(self.get_neighbours(current_cell))
            wall = Cell((neighbour.x + current_cell.x) / 2, (neighbour.y + current_cell.y) / 2, self)
            wall.set_type(PASSAGE)
            self.cells[self.cells.index(wall)] = wall
            current_cell = neighbour
            stack.append(current_cell)
            while len(self.get_neighbours(current_cell)) == 0 and len(stack) != 0:
                current_cell = stack.pop()
        self.cells[self.cells.index(Cell(self.width - 2, self.height - 2, self))].set_type(FINISH)

    def get_neighbours(self, cell):
        x = cell.x
        y = cell.y
        neighbours = []
        for i in range(-2, 3, 4):
            cell1 = Cell(x + i, y, self)
            cell2 = Cell(x, y + i, self)
            if cell1 in self.odd_cells and self.unvisited(cell1):
                neighbours.append(Cell(x + i, y, self))
            if cell2 in self.odd_cells and self.unvisited(cell2):
                neighbours.append(Cell(x, y + i, self))
        return neighbours

    def unvisited(self, cell):
        x = cell.x
        y = cell.y
        if (self.get_cell_type(x + 1, y) == WALL and
                self.get_cell_type(x - 1, y) == WALL and
                self.get_cell_type(x, y + 1) == WALL and
                self.get_cell_type(x, y - 1) == WALL):
            return True
        else:
            return False

    def get_cell_type(self, x, y):
        if Cell(x, y, self) in self.cells:
            index = self.cells.index(Cell(x, y, self))
            return self.cells[index].get_type()


class Cell:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(cell_side_length * self.x, cell_side_length * self.y, cell_side_length,
                                cell_side_length)
        self.cell_type = WALL

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        pygame.draw.rect(screen, self.cell_type, self.rect, 0)

    def set_type(self, cell_type):
        self.cell_type = cell_type

    def get_type(self):
        return self.cell_type


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(25 * self.x, 25 * self.y, 25,
                                25)

    def draw(self):
        self.rect = pygame.Rect(25 * self.x, 25 * self.y, 25,
                                25)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)

    def player_move(self, direction):
        if direction == "up" and current_maze.get_cell_type(self.x, self.y - 1) != WALL:
            self.y -= 1
            print("up")
        elif direction == "down" and current_maze.get_cell_type(self.x, self.y + 1) != WALL:
            self.y += 1
            print("down")
        elif direction == "left" and current_maze.get_cell_type(self.x - 1, self.y) != WALL:
            self.x -= 1
            print("left")
        elif direction == "right" and current_maze.get_cell_type(self.x + 1, self.y) != WALL:
            self.x += 1
            print("right")

    def is_completed(self):
        global current_level, maze_width, maze_height, current_maze, screen_width, screen_height, screen
        if current_maze.get_cell_type(self.x, self.y) == FINISH:
            current_level += 1
            maze_width = 4 * current_level + 1
            maze_height = 4 * current_level + 1
            screen_width, screen_height = cell_side_length * maze_width, cell_side_length * maze_height + 2 * cell_side_length
            screen = pygame.display.set_mode((screen_width, screen_height))
            generate_new_maze(maze_width, maze_height)
            current_maze = mazes[0]
            self.x = 1
            self.y = 1


PASSAGE = (255, 255, 255)
WALL = (170, 170, 170)
FINISH = (85, 235, 52)

player1 = Player(1, 1)
current_level = 1

cell_side_length = 25
maze_width = 4 * current_level + 1
maze_height = 4 * current_level + 1


up = False
down = False
left = False
right = False

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = cell_side_length * maze_width, cell_side_length * maze_height + 2 * cell_side_length
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze')

mazes = []


def generate_new_maze(x, y):
    new_maze = Maze(x, y)
    new_maze.generate()
    if len(mazes) >= 1:
        mazes.pop()
    mazes.append(new_maze)


generate_new_maze(maze_width, maze_height)

current_maze = mazes[0]

while True:
    if up:
        player1.player_move("up")
    if down:
        player1.player_move("down")
    if left:
        player1.player_move("left")
    if right:
        player1.player_move("right")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    player1.is_completed()

    current_maze.draw()
    player1.draw()

    pygame.display.flip()
    clock.tick(16)


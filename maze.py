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
        self.cells[self.cells.index(Cell(self.width - 2, self.height - 2, maze))].set_type(FINISH)

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
            index = self.cells.index(Cell(x, y, maze))
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
        if direction == "up" and maze.get_cell_type(self.x, self.y - 1) != WALL:
            self.y -= 1
            print("up")
        elif direction == "down" and maze.get_cell_type(self.x, self.y + 1) != WALL:
            self.y += 1
            print("down")
        elif direction == "left" and maze.get_cell_type(self.x - 1, self.y) != WALL:
            self.x -= 1
            print("left")
        elif direction == "right" and maze.get_cell_type(self.x + 1, self.y) != WALL:
            self.x += 1
            print("right")



PASSAGE = (255, 255, 255)
WALL = (170, 170, 170)
FINISH = (85, 235, 52)

player1 = Player(1, 1)


cell_side_length = 25
maze_width = 42
maze_height = 42

while maze_width > 41 or maze_height > 41:
    maze_width = 2 * int(input("Enter maze width: ")) + 1
    maze_height = 2 * int(input("Enter maze height: ")) + 1
    if maze_width > 41 or maze_height > 41:
        print("The maximum dimensions are 20x20.")

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = cell_side_length * maze_width, cell_side_length * maze_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Maze')
maze = Maze(maze_width, maze_height)
maze.generate()
screen.fill((30, 30, 30))


start_menu = True


while True:
    while start_menu:
        event_startmenu = pygame.event.poll()
        start_text1 = pygame.font.SysFont('comicsans', 100).render('Press ENTER to start', 1, (255, 255, 255))
        start_text2 = pygame.font.SysFont('comicsans', 90).render('Press ESC to quit', 1, (255, 255, 255))
        screen.blit(start_text1,
                    (screen_width / 2 - start_text1.get_width() / 2, screen_height / 2 - start_text2.get_height() / 2))
        screen.blit(start_text2,
                    (screen_width / 2 - start_text2.get_width() / 2, screen_height / 3 * 2))
        pygame.display.flip()
        if event_startmenu.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event_startmenu.type == pygame.KEYDOWN:
            if event_startmenu.key == pygame.K_RETURN:
                start_menu = False
                break
            if event_startmenu.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.player_move("up")
            if event.key == pygame.K_s:
                player1.player_move("down")
            if event.key == pygame.K_a:
                player1.player_move("left")
            if event.key == pygame.K_d:
                player1.player_move("right")

    screen.fill((30, 30, 30))

    maze.draw()
    player1.draw()

    pygame.display.flip()
    clock.tick(60)

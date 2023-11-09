import pygame
import random
from copy import copy
import pickle
import os


BOARD_SIZE = 100
FPS = 60
CELL_SIZE =6
SCREEN_X = BOARD_SIZE*CELL_SIZE
SCREEN_Y = BOARD_SIZE*CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
advancing = False
relative_coords = [(-1, -1), (0, -1), (1, -1),
                   (-1, 0),           (1, 0),
                   (-1, 1),  (0, 1),  (1, 1)]


def draw_square(screen, top, left, colour):
    pygame.draw.rect(screen, colour, pygame.Rect(
        top, left, CELL_SIZE, CELL_SIZE))


def tuple_addition(a, b):
    return tuple([sum(x) for x in zip(a, b)])


def draw_screen(screen):
    screen.fill(BLACK)
    for cell_x, cell_y in alive_cells:
        draw_square(screen, cell_x*CELL_SIZE, cell_y*CELL_SIZE, WHITE)
    pygame.display.update()


def wait_for_number_input():
    pygame.display.set_caption('Waiting for number input...')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key-48 in range(0, 10):
                    return event.key-48
                if event.key == pygame.K_ESCAPE:
                    return


def save_state(file_number):
    file_name = f'gol_save_{file_number}'
    with open(file_name, 'wb') as f:
        pickle.dump(alive_cells, f)


def load_state(file_number):
    file_name = f'gol_save_{file_number}'
    try:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def advance():
    global counter
    previous_boards.append(copy(alive_cells))
    old_board = copy(alive_cells)
    for x in range(0, BOARD_SIZE):
        for y in range(0, BOARD_SIZE):
            alive_neighbours = 0
            for neighbour in neighbours[(x, y)]:
                if neighbour in old_board:
                    alive_neighbours += 1

            if alive_neighbours == 3:
                alive_cells.add((x, y))
            elif (x, y) in old_board and alive_neighbours == 2:
                alive_cells.add((x, y))
            else:
                try:
                    alive_cells.remove((x, y))
                except KeyError:  # Dead stays dead
                    pass
    counter += 1


def previous():
    global counter
    counter -= 1
    if counter < 0:
        counter = 0
    try:
        return previous_boards.pop()
    except IndexError:  # No more previous
        return alive_cells


def reset():
    global counter
    counter = 0
    alive_cells = set()

    for x in range(0, BOARD_SIZE):
        for y in range(0, BOARD_SIZE):
            if random.choice([True, False]):
                alive_cells.add((x, y))
    return alive_cells


previous_boards = []
running = True
neighbours = dict()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("What does it all mean...")
running = True
counter = 0
alive_cells = reset()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

for x in range(0, BOARD_SIZE):
    for y in range(0, BOARD_SIZE):
        neighbours[(x, y)] = [tuple_addition((x, y), coord)
                              for coord in relative_coords]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                advancing = not advancing
            if event.key == pygame.K_n:
                advance()
            if event.key == pygame.K_r:
                previous_boards = []
                alive_cells = reset()
            if event.key == pygame.K_p:
                advancing = False
                alive_cells = previous()
            if event.key == pygame.K_f:
                pygame.display.set_caption(
                    f"What does it all mean...  {counter} Generations {'Paused' if not advancing else ''} Zooming")
                for i in range(500):
                    advance()
                pygame.display.set_caption(
                    f"What does it all mean...  {counter} Generations {'Paused' if not advancing else ''}")
            if event.key == pygame.K_c:
                alive_cells = set()
                previous_boards = []
                counter = 0
                advancing = False
            if event.key == pygame.K_s:
                save_number = wait_for_number_input()
                if save_number is not None:
                    save_state(save_number)
            if event.key == pygame.K_l:
                save_number = wait_for_number_input()
                if save_number is not None:
                    state = load_state(save_number)
                    if state is not None:
                        alive_cells = copy(state)
                        advancing = False
                        counter = 0
                        previous_boards = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                cell = (x//CELL_SIZE, y//CELL_SIZE)
                if cell in alive_cells:
                    alive_cells.remove(cell)
                else:
                    alive_cells.add(cell)
    if advancing:
        advance()
    draw_screen(screen)
    pygame.display.set_caption(
        f"What does it all mean...  {counter} Generations {'Paused' if not advancing else ''}")
    # clock.tick(FPS)
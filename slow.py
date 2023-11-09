import tkinter as tk
import random

root = tk.Tk()
root.title('Game of Life')
root.resizable(False, False)
COLUMN = 0
ROW = 1
TILE_SIZE = 5
GRID_SIZE = 50
DELAY = 50
playing = True


class Tile(tk.Canvas):
    relative_coord = [(-1, -1), (0, -1), (1, -1),
                      (-1, 0),         (1, 0),
                      (-1, 1), (0, 1), (1, 1)]

    def __init__(self, parent, row, column, alive):
        super().__init__(parent, width=TILE_SIZE, height=TILE_SIZE)
        self.row = row
        self.column = column
        self.alive = alive
        self.neighbour_coords = []
        if self.alive:
            self.config(bg='white')
        else:
            self.config(bg='black')

        self.calculate_neighbours()

    def __repr__(self) -> str:
        return f'Tile row: {self.row}, column: {self.column}'

    def calculate_neighbours(self):
        for rel_coord in Tile.relative_coord:
            new_coord = tuple_addition(rel_coord, (self.row, self.column))
            if -1 in new_coord:
                continue
            if new_coord[COLUMN] > GRID_SIZE-1 or new_coord[ROW] > GRID_SIZE - 1:
                continue
            self.neighbour_coords.append(new_coord)

    def set_state(self, alive):
        if alive:
            self.alive = True
            self.config(bg='white')
        else:
            self.alive = False
            self.config(bg='black')


def tuple_addition(a, b):
    return tuple([sum(x) for x in zip(a, b)])


def advance():
    old_board = generate_boolean_board()
    for row_idx, row in enumerate(old_board):
        for value_idx, value in enumerate(row):
            tile = board[row_idx][value_idx]
            alive_neighbours = 0
            for neighbour in tile.neighbour_coords:
                neighbour_row, neighbour_column = neighbour
                if old_board[neighbour_row][neighbour_column]:
                    alive_neighbours += 1

            if alive_neighbours == 3:
                tile.set_state(True)
            elif value and alive_neighbours == 2:
                tile.set_state(True)
            else:
                tile.set_state(False)
    # print('Advance')
    if playing:
        root.after(DELAY, advance)


def generate_boolean_board():
    boolean_board = []
    for row in board:
        boolean_row = []
        for tile in row:
            boolean_row.append(tile.alive)
        boolean_board.append(boolean_row)
    return boolean_board


def play():
    global playing
    playing = True
    advance()


def pause():
    global playing
    playing = False


def reset():
    global board
    board = []
    for row_idx in range(GRID_SIZE):
        row = []
        for column_idx in range(GRID_SIZE):
            tile = Tile(game_frame, row_idx, column_idx,
                        random.choice([True, False]))
            tile['highlightthickness'] = 0
            tile.grid(row=row_idx, column=column_idx, padx=(
                0, 0), pady=(0, 0), ipadx=0, ipady=0)
            row.append(tile)
        board.append(row)


control_frame = tk.Frame(root)
game_frame = tk.Frame(root)

play_button = tk.Button(control_frame, text='Play', command=play)
pause_button = tk.Button(control_frame, text='Pause', command=pause)
advance_one_button = tk.Button(
    control_frame, text='Advance one generation', command=advance)
reset_button = tk.Button(control_frame, text='Reset', command=reset)

play_button.grid(row=0, column=0)
pause_button.grid(row=0, column=1)
advance_one_button.grid(row=0, column=2)
reset_button.grid(row=0, column=3)

reset()

control_frame.pack()
game_frame.pack()

if playing:
    root.after(DELAY, advance)
root.mainloop()
print()

import numpy as np

sudoku = np.zeros((9,9), dtype=int)
constraints = {} # Dictionary that maps indices of a square to a set of indices by which it is constraint

def pretty_print(sudoku):
    output = "╔═══════╦═══════╦═══════╗\n"
    for i in range(0,9):
        if i == 3 or i == 6:
            output += "╠═══════╬═══════╬═══════╣\n"
        output += "║ "
        for j in range(0,9):
            if j == 3 or j == 6:
                output += "║ "
            output += str(sudoku[i][j]) + " "
        output += "║\n"
    output += "╚═══════╩═══════╩═══════╝\n"
    print(output)

def parse_sudoku(filepath: str):
    with open(filepath) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            for j, val in enumerate(line.strip()):
                sudoku[i][j] = val

def initialise_neighbours(board):
    for i,j in np.ndindex(board.shape):
        neighbours = set()
        for k in range(0,9): 
            if k == j:
                continue
            neighbours.add((i,k)) # Add all vertical neighbours from the column
        for k in range(0,9):
            if k == i:
                continue
            neighbours.add((k,j)) # Add all horizontal neighbours from the row
        for row in range(i //3 * 3, i//3*3 + 3): # Identify the top left corner of a 3x3 box 
            for col in range(j //3 * 3, j//3 * 3 + 3):
                if row == i and col == j:
                    continue
                neighbours.add((row,col))
        constraints[(i,j)] = neighbours

def valid_sudoku(sudoku):
    # first we check whether each row is valid
    for i in range(0,9):
        valid_nrs = set()
        for j in range(0,9):
            if sudoku[i,j] != 0:
                valid_nrs.add(sudoku[i,j])
        if len(valid_nrs) < 9:
            return False
    # Then we check each column
    for j in range(0,9):
        valid_nrs = set()
        for i in range(0,9):
             if sudoku[i,j] != 0:
                valid_nrs.add(sudoku[i,j])
        if len(valid_nrs) < 9:
            return False
    # And finally we check each 3x3 grid
    for i in range(0,9,3):
        for j in range(0,9,3):
            valid_nrs = set()
            for row in range(i,i+3):
                for col in range(j,j+3):
                    if sudoku[i,j] != 0:
                        valid_nrs.add(sudoku[row,col])
            if len(valid_nrs) < 9:
                return False
    return True 
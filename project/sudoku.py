import numpy as np


def pretty_print(sudoku):
    output = "╔═══════╦═══════╦═══════╗\n"
    for i in range(0, 9):
        if i == 3 or i == 6:
            output += "╠═══════╬═══════╬═══════╣\n"
        output += "║ "
        for j in range(0, 9):
            if j == 3 or j == 6:
                output += "║ "
            output += str(sudoku[i][j]) + " "
        output += "║\n"
    output += "╚═══════╩═══════╩═══════╝\n"
    print(output)


def parse_sudoku(filepath: str):
    """
    Reads a sudoku from the given filepath and creates a 2D np.array
    filled with the values it reads. In case a field is not filled in yet,
    it has the default value of 0
    """
    sudoku = np.zeros((9, 9), dtype=int)
    with open(filepath) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            for j, val in enumerate(line.strip()):
                sudoku[i][j] = val
    return sudoku


def initialise_constraints(board):
    """
    Given a sudoku grid, for each field A, find all fields B that constrain A.
    Constraining in this context means that A may not have the same value as B (and vice versa).
    In the case of the sudoku, B consists of the fields that are in the same row, column or 3x3
    grid as A. A is stored as a tuple of the index of A in the board, and B is a list of indices
    of all the constraints.
    """
    constraints = (
        {}
    )  # Dictionary that maps indices of a square to a set of indices by which it is constrained
    for i, j in np.ndindex(board.shape):
        neighbours = set()
        for k in range(0, 9):
            if k == j:
                continue
            neighbours.add((i, k))  # Add all vertical neighbours from the column
        for k in range(0, 9):
            if k == i:
                continue
            neighbours.add((k, j))  # Add all horizontal neighbours from the row
        for row in range(
            i // 3 * 3, i // 3 * 3 + 3
        ):  # Identify the top left corner of a 3x3 box
            for col in range(j // 3 * 3, j // 3 * 3 + 3):
                if row == i and col == j:
                    continue
                neighbours.add((row, col))
        constraints[(i, j)] = neighbours
    return constraints


def valid_sudoku(sudoku):
    """
    Check whether a proposed solution is a valid solution to the sudoku.
    A solution is valid iff: for each row, column and 3x3 grid, the values
    1-9 occur exactly once.
    """
    # first we check whether each row is valid
    for i in range(0, 9):
        valid_nrs = set()
        for j in range(0, 9):
            if sudoku[i, j] != 0:
                valid_nrs.add(sudoku[i, j])
        if len(valid_nrs) < 9:
            return False
    # Then we check each column
    for j in range(0, 9):
        valid_nrs = set()
        for i in range(0, 9):
            if sudoku[i, j] != 0:
                valid_nrs.add(sudoku[i, j])
        if len(valid_nrs) < 9:
            return False
    # And finally we check each 3x3 grid
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            valid_nrs = set()
            for row in range(i, i + 3):
                for col in range(j, j + 3):
                    if sudoku[i, j] != 0:
                        valid_nrs.add(sudoku[row, col])
            if len(valid_nrs) < 9:
                return False
    return True


def is_valid_value(sudoku, constraints, index):
    """
    A value is valid iff: it is not zero, and it does not conflict with any
    of its neighbours (conflict : having the same value as the neighbour).
    The neighbours are stored within a constraints dictionary, that maps a
    tuple of (x,y) coordinates (index) of the field to the (x,y) coordinates of all its
    neighbours.
    """
    neighbours = constraints[index]
    if sudoku[index] == 0:
        return False
    for n in neighbours:  # Here, n is actually a tuple of two ints
        if sudoku[index] == sudoku[n]:
            return False
    return True


def fitness_from_sudoku(sudoku):
    """
    For each field in a sudoku, we check if the value in it is valid.
    For a value to be valid, see the explanation at is_valid_value.
    The fitness is the count of valid values in a sudoku, and is thus
    in the interval [0,81], where 81 indicates that a solution is found for the sudoku
    """
    score = 0
    constraints = initialise_constraints(sudoku)
    for key in constraints.keys():
        if is_valid_value(sudoku, constraints, key):
            score += 1
    return score

def fitness_from_values(sudoku, open_fields, values):
    new_sudoku = sudoku.copy()
    for index, val in zip(open_fields, values):
        new_sudoku[index] = val
    return fitness_from_sudoku(new_sudoku)

def determine_open_fields(sudoku):
    """
    Identifies all fields that do not have a value (i.e. value = 0) in
    the original sudoku configuration. These fields are stored as a tuple
    of (x,y) coordinates and returned in a list
    """
    open_fields = []
    for i, j in np.ndindex(sudoku.shape):
        if sudoku[i, j] == 0:
            open_fields.append((i, j))
    return open_fields


def available_values(sudoku):
    """
    Collects all available values for a given sudoku.
    A completely empty sudoku thus returns a list that contains:
    9 times 1, 9 times 2, 9 times 3 etc. For each value that we encounter
    in the initial sudoku configuration, we remove that value from the list
    """
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9] * 9
    for i, j in np.ndindex(sudoku.shape):
        if sudoku[i, j] != 0:
            values.remove(sudoku[i, j])
    return sorted(values)

def is_solution(sudoku, open_fields, values):
    s = sudoku.copy()
    for index, val in zip(open_fields, values):
        s[index] = val
    return valid_sudoku(s)

def fill_in_sudoku(sudoku, open_fields, values):
    s = sudoku.copy()
    for index, val in zip(open_fields, values):
        s[index] = val
    return s

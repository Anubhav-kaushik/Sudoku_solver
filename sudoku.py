# imported module
import numpy as np
import sys

# inputs
sudoku_problem = np.array([[4, 7, 0, 3, 5, 0, 2, 1, 8],
                           [5, 8, 0, 4, 0, 1, 7, 0, 3],
                           [1, 3, 0, 0, 8, 0, 0, 4, 5],
                           [0, 1, 0, 7, 0, 0, 3, 8, 0],
                           [6, 0, 3, 0, 1, 5, 4, 0, 0],
                           [7, 4, 0, 0, 3, 0, 0, 0, 1],
                           [8, 0, 1, 0, 0, 0, 5, 3, 9],
                           [0, 0, 7, 5, 0, 0, 1, 0, 4],
                           [0, 5, 4, 1, 0, 3, 0, 7, 0]], dtype='int32')

# Take input from user in one line
inp = input(f"Enter the values row wise without space or any separator: ")

if len(inp) != 0:
    for row_ in range(9):
        for col, k in zip(range(9), range(9*row_, 9*(row_ + 1))):
            sudoku_problem[row_, col] = int(inp[k])


# Functions
def coordinates_2be_filled(sudoku_puzzle):
    """
        This function find the empty squares and filled squares of a sudoku puzzle.
    :param sudoku_puzzle: 9X9 numpy array containing sudoku problem
    :return: 2 list, first containing empty squares position and second containing filled squares position
    """
    empty_squares = []
    filled_squares = []
    coordinate_3_3 = [[i, j] for i in range(3) for j in range(3)]
    for box_r, box_c in coordinate_3_3:
        for r, c in coordinate_3_3:
            if sudoku_puzzle[r + (3 * box_r), c + (3 * box_c)] == 0:
                empty_squares.append([r + (3 * box_r), c + (3 * box_c)])
            else:
                filled_squares.append([r + (3 * box_r), c + (3 * box_c)])

    return empty_squares, filled_squares


def possibility(sudoku_puzzle):
    """
        This function find the probability of a cell to fill.
    :param sudoku_puzzle: 9X9 numpy array containing sudoku problem
    :return: 2 dict, first contains probability of all empty cells and second contains possible digits that may fill in
             the empty cells.
    """
    global coordinates_tobe_filled

    dict_digit = {}
    probability = {}

    if 0 not in sudoku_puzzle:
        probability = {'finish': 0.05}
        dict_digit = {'finish': 0}
        return probability, dict_digit

    for r, c in coordinates_tobe_filled:
        row = sudoku_puzzle[r, :]
        column = sudoku_puzzle[:, c]
        box_r = r // 3
        box_c = c // 3
        box = sudoku_puzzle[3 * box_r: 3 + (3 * box_r), 3 * box_c: 3 + (3 * box_c)]
        if sudoku_puzzle[r, c] == 0:
            digits = []
            for i in range(1, 10):
                if i not in row and i not in column and i not in box:
                    digits.append(i)
            if len(digits) == 0:
                probability = {'wrong path': 2}
                dict_digit = {'wrong path': 1}
                return probability, dict_digit

            probability[f'{r}{c}'] = 1 / len(digits)
            dict_digit[f'{r}{c}'] = digits.copy()

        else:
            probability[f'{r}{c}'] = 0

    return probability, dict_digit


def solver():
    probability, corresponding_digits = possibility(sudoku_problem)
    min_chances = int(1/max(probability.values()))

    if min_chances == 0:
        return False

    # when the solver found a solution it return min_chances = 20
    if min_chances == 20:
        solutions.append(sudoku_problem.copy())
        return False

    for key in probability.keys():
        if probability[key] == max(probability.values()):
            for digit in corresponding_digits[key]:
                sudoku_problem[int(key[0]), int(key[1])] = digit
                if solver():
                    return True
                sudoku_problem[int(key[0]), int(key[1])] = 0
            return False


if __name__ == '__main__':
    solutions = []
    coordinates_tobe_filled, _ = coordinates_2be_filled(sudoku_problem)

    sys.setrecursionlimit(1000000)

    solver()

    total_sol = len(solutions)

    n = int(input(f"How many solution do you want? There are {total_sol} solutions available.\n"))

    for sol in range(n):
        print(solutions[sol])
        print("\n")

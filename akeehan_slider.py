#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2.667 template
Alexander Keehan, University of Mary Washington, fall 2023
'''

from copy import deepcopy
from puzzle import Puzzle
import sys


def solve(p):
    '''Finds a sequence of moves ("L", "U", "R", or "D") that will solve the
    Puzzle object passed. Returns that sequence in a list.
    '''
    # Define what a state of the board is
    class State:
        def __init__(self, state, parent=None, cost=0, heuristic=0):
            self.state = state
            self.parent = parent
            self.cost = cost
            self.heuristic = heuristic

    # Get neighbors
    def get_neighbors():
        return p.legal_moves()

    # Calculate distance
    def calculate_distance(node, puzzle, solved):
        solved = solved.grid
        # Find current pos
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                if puzzle[x][y] == node:
                    curr_row = x
                    curr_col = y
                    break

        # Find goal pos
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                if solved[x][y] == node:
                    row = x
                    col = y
                    break

        # Find difference between curr and goal pos
        distance = abs(curr_row - row) + abs(curr_col - col)
        return distance

    # Get heuristic cost
    def get_heuristic(puzzle):
        puzzle = puzzle.grid
        solved = Puzzle(len(puzzle))
        total_dist = 0
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                node = puzzle[x][y]
                if node != -1:
                    total_dist += calculate_distance(node, puzzle, solved)
                    print(total_dist)
        
        return total_dist




    # Do A* Search
    def astar ():
        return 0
    

 
    heuristic = get_heuristic(p)
    print("Result", result)
    # Here's a (bogus) example return value:
    return ["D","U","L","L"]



if __name__ == '__main__':

    if (len(sys.argv) not in [2,3]  or
        not sys.argv[1].isnumeric()  or
        len(sys.argv) == 3 and not sys.argv[2].startswith("seed=")):
        sys.exit("Usage: puzzle.py dimensionOfPuzzle [seed=###].")

    n = int(sys.argv[1])

    if len(sys.argv) == 3:
        seed = int(sys.argv[2][5:])
    else:
        seed = 123

    # Create a random puzzle of the appropriate size and solve it.
    puzzle = Puzzle.gen_random_puzzle(n, seed)
    print(puzzle)
    solution = solve(puzzle)
    if puzzle.has_solution(solution):
        input("Yay, this puzzle is solved! Press Enter to watch.")
        puzzle.verify_visually(solution)
    else:
        print(f"Sorry, {''.join(solution)} does not solve this puzzle.")

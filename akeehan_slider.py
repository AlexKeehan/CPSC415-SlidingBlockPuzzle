#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2.667 template
Alexander Keehan, University of Mary Washington, fall 2023
'''

from copy import deepcopy
from puzzle import Puzzle
import sys
import heapq


def solve(p):
    '''Finds a sequence of moves ("L", "U", "R", or "D") that will solve the
    Puzzle object passed. Returns that sequence in a list.
    '''

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
        # Check distance between everything to get total heuristic
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                node = puzzle[x][y]
                if node != -1:
                    total_dist += calculate_distance(node, puzzle, solved)
        
        return total_dist

    # Do A* Search
    def a_star(p):
        # Frontier stores states to be expanded
        frontier = [(get_heuristic(p), ())]
        # visited stores sequences we have seen before
        visited = set()
        # frontierPuzzles stores puzzles and sequences
        frontierPuzzles = {() : deepcopy(p)}

        # Loop until solution found
        while frontier:
            # Use _ to chew up the heuristic and set curr_state to the sequence in the frontier
            _, curr_state = heapq.heappop(frontier)            
             
            # curr_puzzle stores the puzzle we are on
            curr_puzzle = frontierPuzzles[curr_state]
            
            # Check if we are in goal state
            if get_heuristic(curr_puzzle) == 0:
                return curr_state
            
            # Add sequence to visited
            visited.add(curr_state)
                        
            # moves stores all possible moves from current puzzle
            moves = curr_puzzle.legal_moves()
            
            # Loop through all the moves
            for move in moves:
                # flag checks if a puzzle has been visited before
                flag = 0
                # deepcopy the puzzle
                puzzle = deepcopy(curr_puzzle)
                # Do the move on the copied puzzle
                puzzle.move(move)
                
                # Loop through frontierPuzzles to check if the new puzzle is already in it
                for p in frontierPuzzles:
                    temp_puzzle = frontierPuzzles[p]
                    if puzzle.__eq__(temp_puzzle):
                        flag = 1    
                
                # Add the sequence to new_state
                new_state = curr_state + (move,)
                
                # Get the heuristic for new sequence
                heuristic = len(new_state) + get_heuristic(puzzle)
            
                # Check if the new sequence is in visited or if the puzzle has been visited before
                if new_state not in visited and flag == 0:
                    # If not, then add it to the frontier
                    heapq.heappush(frontier, (heuristic, new_state))
                    # Also add it to frontierPuzzles
                    frontierPuzzles[new_state] = puzzle


    # ans stores the final sequence to solve the puzzle
    ans = []
    # Call a_star
    ans = a_star(p)
    return ans
    # Here's a (bogus) example return value:
    #return ["D","U","L","L"]



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

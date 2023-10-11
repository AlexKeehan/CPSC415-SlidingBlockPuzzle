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
        for x in range(len(puzzle)):
            for y in range(len(puzzle[x])):
                node = puzzle[x][y]
                if node != -1:
                    total_dist += calculate_distance(node, puzzle, solved)
        
        return total_dist

    def insert_frontier(frontier, frontierEstimates, frontierPuzzles, state, heuristic):
        for x in range(len(frontier)):
            #frontier_heuristic = get_heuristic(x)
            #if heuristic > frontier_heuristic:
            if frontierEstimates[frontier[x]] > heuristic:
                frontier.insert(x, state)
                frontierEstimates[state] = heuristic
                frontierPuzzles[state] = deepcopy(frontierPuzzles[frontier[x]])
                return
        frontier.append(state)
        frontierEstimates[state] = heuristic
        frontierPuzzles[state] = deepcopy(frontierPuzzles[frontier[-1]])


    # Do greedy Search
    def solve(p):
        frontier = [(get_heuristic(p), ())]
        frontierEstimates = {() : 0}
        frontierPuzzles = {() : p}
        
        while frontier:
            print("Frontier", frontier)
            _, curr_state = heapq.heappop(frontier)
            
            curr_puzzle = frontierPuzzles[curr_state]

            test = get_heuristic(curr_puzzle)
            print("Heuristic", test)
            if curr_puzzle.is_solved():
                return curr_state
            #if get_heuristic(curr_puzzle) == 0:
                return curr_state
            
            moves = curr_puzzle.legal_moves()
            length_moves = len(moves)
            for move in moves:
                puzzle = deepcopy(curr_puzzle)
                puzzle.move(move)
                
                new_state = curr_state + (move,)
                
                heuristic = get_heuristic(puzzle)

                frontierEstimates[new_state] = heuristic
                frontierPuzzles[new_state] = puzzle
                heapq.heappush(frontier, (heuristic, new_state))

    ans = []
    ans = solve(p)

    return ans
    #heuristic = get_heuristic(p)
    #print("Result", heuristic)
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
